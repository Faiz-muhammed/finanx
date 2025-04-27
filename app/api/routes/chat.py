from fastapi import APIRouter, WebSocket, WebSocketDisconnect, UploadFile, Depends, HTTPException, BackgroundTasks, File
from fastapi.responses import StreamingResponse
from app.api.utils.socket import connectionManager
from config import settings  # Import directly from the config package
# from typing import Dict, List, Optional, Any
# import json
# import base64
import os
# from datetime import datetime
# from app.services.trial_balance_analysis import extract_columns_to_csv
# from google import genai
import google.generativeai as genai
# from google.generativeai import types
import pandas as pd
# from tabulate import tabulate
from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
import zipfile
from io import StringIO
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# Import the storage module
from app.api.utils.storage import storage
from app.api.utils.pdf import pdfUtils
from app.agents.base import FinancialStatementsAgent
from app.agents.financial_forcast import FinancialForcastAgent
import uuid

router = APIRouter()

websocketManager = connectionManager()

# Configure Gemini API Key (Replace with your actual key)
GENAI_API_KEY = settings.API_KEY
genai.configure(api_key=GENAI_API_KEY)

@router.post("/generate-reports")
async def generate_reports(
    background_tasks: BackgroundTasks,
    trail_b_file: UploadFile = File(...),
    report_id: str = None, 
):
    try:

        if not report_id:
            report_id = str(uuid.uuid4())

        # Read the uploaded Excel file
        contents = await trail_b_file.read()
        xls = pd.ExcelFile(BytesIO(contents))
        df = pd.read_excel(xls, sheet_name=xls.sheet_names[0], header=None)

        # Locate the header row dynamically
        header_row_idx = df[df.iloc[:, 1] == "Ledger Name"].index[0]

        # Extract trial balance data
        trial_balance = df.iloc[header_row_idx:, 1:5]
        trial_balance.columns = ["Ledger Name", "Ledger Type", "Debit", "Credit"]
        trial_balance = trial_balance[1:].reset_index(drop=True)

        # Convert trial balance to text format
        trial_balance_text = trial_balance.to_string(index=False)

        # Get AI-generated P&L statement
        pl_statement = FinancialStatementsAgent.generate_PnL_statement(trial_balance_text)
        storage.save_report(report_id, "balance_sheet", trial_balance_text, pl_statement)
        df_pl_statement = pd.read_csv(StringIO(pl_statement))

        balance_sheet = FinancialStatementsAgent.generate_balance_sheet(trial_balance_text)
        storage.save_report(report_id, "balance_sheet", trial_balance_text, balance_sheet)
        df_balance_sheet = pd.read_csv(StringIO(balance_sheet))

        # Convert P&L to PDF
        pdf_buffer = pdfUtils.create_pdf_df(df_pl_statement,"Profit & Loss Statement")
        balance_sheet_pdf_buffer = pdfUtils.create_pdf_df(df_balance_sheet,"Balance Sheet")

        print(balance_sheet_pdf_buffer,'balance_sheet_pdf_buffer')

         # Create a zip file containing both PDFs
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            zip_file.writestr("profit_loss_statement.pdf", pdf_buffer.getvalue())
            zip_file.writestr("balance_sheet.pdf", balance_sheet_pdf_buffer.getvalue())
    
        zip_buffer.seek(0)

        print(zip_buffer,'zip_buffer')
    
        # Return the zip file as a downloadable response
        return StreamingResponse(zip_buffer, media_type="application/zip", headers={
        "Content-Disposition": "attachment; filename=financial_statements.zip"
         })

    except Exception as e:
        return {"error": str(e)}


@router.post("/generate-forecast-data")
async def generate_advanced_reports(
    background_tasks: BackgroundTasks,
    # trail_b_file: UploadFile = File(...),
    report_Id: str,
    report_type: str,  # "tax_analysis", "financial_forecast", etc.
):
    try:
        # Get user's previous reports as context
        user_reports = storage.get_all_user_reports(report_Id)

        print(user_reports,'userReports')
            
        # Build context from previous reports
        context = ""
        for rep_type, report_info in user_reports.items():
            context += f"Previous {rep_type} data:\n{report_info['report_data']}\n\n"
                
            # Generate new report with historical context
            print(f"Generating new {report_type} with historical context")
         
            report_data = FinancialForcastAgent.get_financial_forecast(user_reports.profit_and_loss,user_reports.balance_sheet, context, report_type)
                
            # Store the new report
            # storage.save_report(report_Id, report_type, user_reports, report_data)
        
        # Convert to PDF and return
        df_report = pd.read_csv(StringIO(report_data))
        pdf_buffer = pdfUtils.create_pdf_df(df_report, f"{report_type.replace('_', ' ').title()}")
        pdf_buffer.seek(0)
        
        return StreamingResponse(
            pdf_buffer, 
            media_type="application/pdf", 
            headers={"Content-Disposition": f"attachment; filename={report_type}.pdf"}
        )
        
    except Exception as e:
        return {"error": str(e)}