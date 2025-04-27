import json
import google.generativeai as genai

class FinancialForcastAgent:
    def get_financial_forecast(
    profit_and_loss_data: list,
    balance_sheet_data: list,
    forecast_years: int,
    ) -> dict:
   
        model = genai.GenerativeModel("gemini-1.5-flash")
    
        # Construct the prompt with detailed instructions and schema
        prompt = f"""
        You are an expert financial analyst tasked with generating a financial forecast based on provided Profit and Loss (Income Statement) and Balance Sheet data. Your output must be a JSON object adhering strictly to the schema defined below.

        **Provided Financial Data:**

        ```json
        {{
        "profit_and_loss": {json.dumps(profit_and_loss_data)},
        "balance_sheet": {json.dumps(balance_sheet_data)}
        }}
        ```

        **Instructions:**

        1.  Analyze the provided historical financial data. Identify key trends, growth rates, and relationships between different financial statement line items.
        2.  Generate a financial forecast for the next {forecast_years} years. Be realistic and provide clear assumptions for your projections. Consider potential growth scenarios, cost efficiencies, and any other relevant factors that might influence future performance.
        3.  Focus on forecasting the following key financial metrics:
            * Revenue
            * Cost of Goods Sold
            * Gross Profit
            * Operating Expenses
            * Operating Income
            * Net Income
            * Total Current Assets
            * Total Assets
            * Total Current Liabilities
            * Total Liabilities
            * Equity
        4.  Present your forecast exclusively as a JSON object that strictly adheres to the following schema. Do not include any introductory or explanatory text outside of the JSON structure.

        **JSON Output Schema:**

        ```json
        {{
        "forecast": [
            {{
            "year": NUMBER,
            "revenue": NUMBER,
            "cost_of_goods_sold": NUMBER,
            "gross_profit": NUMBER,
            "operating_expenses": NUMBER,
            "operating_income": NUMBER,
            "net_income": NUMBER,
            "total_current_assets": NUMBER,
            "total_assets": NUMBER,
            "total_current_liabilities": NUMBER,
            "total_liabilities": NUMBER,
            "equity": NUMBER
            }},
            // ... forecast data for the specified number of years
        ],
        "assumptions": [
            {{"metric": "STRING", "year": NUMBER, "value": "STRING"}},
            // ... clearly state the key assumptions used for each forecasted year and metric
        ],
        "disclaimer": "STRING"
        }}
        ```

        **Important Notes:**

        * Ensure that all NUMBER values in the JSON output are represented as either integers or floating-point numbers.
        * Provide realistic financial values in your forecast.
        * The "assumptions" section is crucial.  For each year in the forecast, provide at least 3 key assumptions (e.g., Revenue Growth Rate, COGS as a percentage of Revenue, Operating Expenses Growth Rate).
        * The "disclaimer" should be a single string.

        Output:
        """

        try:
            response = model.generate_content(prompt)
            # Attempt to parse the response as JSON
            forecast_data = json.loads(response.text)
            # Basic validation of the top-level structure.
            if not isinstance(forecast_data, dict):
                return {
                    "status": "error",
                    "message": "The response was not a valid JSON object."
                }

            #Check for the required keys
            required_keys = ["forecast", "assumptions", "disclaimer"]
            if not all(key in forecast_data for key in required_keys):
                return {
                    "status": "error",
                    "message": f"The response is missing one or more required keys: {required_keys}"
                }

            return {
                "status": "success",
                "data": forecast_data,
            }
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": f"Error decoding JSON response: {e}.  Raw response text: {response.text}",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"An unexpected error occurred: {e}",
            }