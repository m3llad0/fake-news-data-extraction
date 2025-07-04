import gspread
from app.config import Config
import logging

class GoogleSheetsManager:
    """
    A class to manage interactions with Google Sheets using gspread.
    Provides methods to open spreadsheets, retrieve worksheets,
    get rows, and append new rows to a specified worksheet.
    """
    
    def __init__(self, spreadsheet_name=None):
        """
        Initializes the GoogleSheetsManager with service account credentials.
        """
        if not Config.SERVICE_ACCOUNT:
            raise ValueError("Service account path is not set in the configuration.")
        
        self.client = gspread.service_account(filename=Config.SERVICE_ACCOUNT)
        try:
            self.spreadsheet = self.client.open_by_url(spreadsheet_name)
        except Exception as e:
            raise ValueError(f"Failed to open spreadsheet '{spreadsheet_name}': {e}")
        
    def get_worksheet(self, worksheet_name):
        """
        Gets a worksheet by its name. If not found, creates a new one.
        """
        if not self.spreadsheet:
            raise ValueError("No spreadsheet is currently opened.")
        
        try:
            return self.spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            logging.error(f"Worksheet '{worksheet_name}' not found. Creating a new worksheet.")
            return self.spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

    def get_rows(self, worksheet_name):
        """
        Retrieves all records from the given worksheet as a list of dicts.

        :param worksheet_name: Name of the worksheet to retrieve from.
        :return: List[Dict[str, Any]]
        """
        worksheet = self.get_worksheet(worksheet_name)
        return worksheet.get_all_records()

    def append_row(self, worksheet_name, row_data):
        """
        Appends a new row to the specified worksheet.

        :param worksheet_name: Name of the worksheet.
        :param row_data: List of cell values to append as a row.
        """
        worksheet = self.get_worksheet(worksheet_name)
        worksheet.append_row(row_data)

    def update_row(self, worksheet_name, row, col, value):
        """
        Updates a specific cell in the worksheet.

        :param worksheet_name: Name of the worksheet.
        :param row: Row index (1-based).
        :param col: Column index (1-based).
        :param value: New value to assign.
        """
        worksheet = self.get_worksheet(worksheet_name)
        worksheet.update_cell(row, col, value)
