from datetime import datetime
import json
import os

class InMemoryStorage:
    """
    Simple in-memory storage for financial reports with optional file persistence.
    This class serves as a temporary database replacement during development.
    """
    def __init__(self, persist_to_file=True, storage_file="reports_storage.json"):
        self.reports = {}  # user_id -> {report_type -> report_data}
        self.persist_to_file = persist_to_file
        self.storage_file = storage_file
        
        # Load existing data if file exists
        if persist_to_file:
            self.load_from_file()
    
    def get_report(self, user_id, report_type):
        """
        Retrieve a specific report for a user if it exists
        
        Args:
            user_id (str): The user's unique identifier
            report_type (str): The type of report (e.g., "profit_loss", "balance_sheet")
            
        Returns:
            dict or None: The report data if found, None otherwise
        """
        if user_id in self.reports and report_type in self.reports[user_id]:
            return self.reports[user_id][report_type]
        return None
    
    def save_report(self, user_id, report_type, trial_balance_text, report_data):
        """
        Save a report for a specific user
        
        Args:
            user_id (str): The user's unique identifier
            report_type (str): The type of report (e.g., "profit_loss", "balance_sheet")
            trial_balance_text (str): The trial balance text used to generate the report
            report_data (str): The generated report data (typically CSV format)
        """
        if user_id not in self.reports:
            self.reports[user_id] = {}
        
        self.reports[user_id][report_type] = {
            "trial_balance_text": trial_balance_text,
            "report_data": report_data,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Persist to file if enabled
        if self.persist_to_file:
            self.save_to_file()
    
    def get_all_user_reports(self, user_id):
        """
        Get all reports for a specific user
        
        Args:
            user_id (str): The user's unique identifier
            
        Returns:
            dict: A dictionary of all reports for the user, or empty dict if none found
        """
        if user_id in self.reports:
            return self.reports[user_id]
        return {}
    
    def delete_report(self, user_id, report_type):
        """
        Delete a specific report for a user
        
        Args:
            user_id (str): The user's unique identifier
            report_type (str): The type of report to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        if user_id in self.reports and report_type in self.reports[user_id]:
            del self.reports[user_id][report_type]
            
            # Clean up empty user entries
            if not self.reports[user_id]:
                del self.reports[user_id]
                
            # Persist changes
            if self.persist_to_file:
                self.save_to_file()
                
            return True
        return False
    
    def save_to_file(self):
        """Save the current state to a JSON file"""
        with open(self.storage_file, "w") as f:
            json.dump(self.reports, f, indent=2)
        
    def load_from_file(self):
        """Load the state from a JSON file if it exists"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r") as f:
                    self.reports = json.load(f)
        except Exception as e:
            print(f"Error loading storage file: {e}")
            self.reports = {}
    
    def clear_all(self):
        """Clear all stored data"""
        self.reports = {}
        if self.persist_to_file and os.path.exists(self.storage_file):
            os.remove(self.storage_file)

# Create a singleton instance
storage = InMemoryStorage()