import pandas as pd
from fastapi import UploadFile,File
import io
import base64
from typing import List, Dict
from pydantic import BaseModel

class FileUpload(BaseModel):
    name: str
    type: str
    size: int
    data: str  # Base64 encoded data

async def process_file(file: UploadFile):
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))  # Adjust based on file type
    transformed_data = transform_dataframe(df)
    return transformed_data

def transform_dataframe(df: pd.DataFrame):
    # Your transformation logic here
    return df.describe().to_dict()  # Example: return summary stats

def extract_columns_to_csv(file_info: Dict, required_columns: List[str]) -> io.StringIO:
    """
    Helper function to extract specific columns from an Excel file and convert to CSV.
    
    Args:
        file_info (Dict): File information containing name, type, size and base64 data
        required_columns (List[str]): List of column names to extract
    
    Returns:
        io.StringIO: CSV data as a StringIO object
    
    Raises:
        ValueError: If any required columns are missing or if the file is not an Excel file
    """
    # Check if the uploaded file is an Excel file
    if not file_info['name'].endswith(('.xlsx', '.xls')):
        raise ValueError("Uploaded file must be an Excel file (.xlsx or .xls)")
    
    # Decode base64 data
    try:
        file_bytes = base64.b64decode(file_info['data'])
    except Exception:
        raise ValueError("Invalid base64 encoded data")
    
    # Create a BytesIO object from the file content
    excel_buffer = io.BytesIO(file_bytes)
    
    # Read the Excel file using pandas
    df = pd.read_excel(excel_buffer)

    print(df,'joop')
    
    # Check if all required columns exist
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Filter the dataframe to keep only the required columns
    filtered_df = df[required_columns]
    
    # Convert the filtered dataframe to CSV
    csv_data = io.StringIO()
    filtered_df.to_csv(csv_data, index=False)
    csv_data.seek(0)
    
    return csv_data

