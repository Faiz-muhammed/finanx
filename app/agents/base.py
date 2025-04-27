# from google import genai
import google.generativeai as genai
# from google.generativeai import types

class FinancialStatementsAgent:
    async def generate_PnL_statement(self, trial_balance_text):
        prompt = f"""
        Given the following trial balance, generate a well-structured Profit & Loss (P&L) statement.

        Return ONLY a properly formatted CSV with no additional text, markdown formatting, code blocks, or explanations. The CSV should have these exact headers and format:

        Category,Description,Amount
        Revenue,Product Sales,000000
        Revenue,Service Income,00000
        Expenses,Purchase,00000
        Expenses,Direct expenses,00000
        Expenses,Indirect expense,00000

        Important: 
        - Include headers exactly as shown
        - Use commas as separators
        - Include the full Category value on each row (don't leave it blank for related items)
        - No code block markers (```), just pure CSV data
        - No explanations before or after the CSV

        Here's the trial balance:
        {trial_balance_text}
        """
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    
    async def generate_balance_sheet(trial_balance_text):
        prompt = f"""
        Given the following trial balance, generate a well-structured Balance Sheet.

        Return ONLY a properly formatted CSV with no additional text, markdown formatting, code blocks, or explanations. The CSV should have these exact headers and format:

        Category,Description,Amount
        Assets,Cash,50000
        Assets,Accounts Receivable,25000
        Assets,Inventory,30000
        Liabilities,Accounts Payable,15000
        Liabilities,Notes Payable,20000
        Equity,Common Stock,50000
        Equity,Retained Earnings,20000

        Important: 
        - Include headers exactly as shown
        - Use commas as separators
        - Include the full Category value on each row (don't leave it blank for related items)
        - No code block markers (```), just pure CSV data
        - No explanations before or after the CSV

        Here's the trial balance:
        {trial_balance_text}
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
        