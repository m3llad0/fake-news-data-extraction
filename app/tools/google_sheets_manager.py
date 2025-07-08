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
        Initialize the GoogleSheetsManager with service account credentials and open the specified Google Spreadsheet by URL.
        
        Parameters:
        	spreadsheet_name (str, optional): The URL of the Google Spreadsheet to open.
        
        Raises:
        	ValueError: If the service account path is not set in the configuration or if the spreadsheet cannot be opened.
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
        Retrieve a worksheet by name from the opened spreadsheet, creating it if it does not exist.
        
        If the specified worksheet is not found, a new worksheet with 100 rows and 20 columns is created and returned.
        
        Parameters:
            worksheet_name (str): The name of the worksheet to retrieve or create.
        
        Returns:
            Worksheet: The requested or newly created worksheet object.
        
        Raises:
            ValueError: If no spreadsheet is currently opened.
        """
        try:
            return self.spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            logging.info(f"Worksheet '{worksheet_name}' not found. Creating a new worksheet.")
            return self.spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

    def get_rows(self, worksheet_name):
        """
        Return all records from the specified worksheet as a list of dictionaries.
        
        Parameters:
            worksheet_name (str): The name of the worksheet to retrieve records from.
        
        Returns:
            List[Dict[str, Any]]: A list where each item is a dictionary representing a row, with keys as column headers.
        """
        worksheet = self.get_worksheet(worksheet_name)
        return worksheet.get_all_records()

    def append_row(self, worksheet_name, row_data):
        """
        Append a new row of data to the specified worksheet.
        
        Parameters:
            worksheet_name (str): The name of the worksheet to append the row to.
            row_data (list): The list of cell values to add as a new row.
        """
        worksheet = self.get_worksheet(worksheet_name)
        worksheet.append_row(row_data)

    def update_row(self, worksheet_name, row, col, value):
        """
        Update the value of a specific cell in a worksheet.
        
        Parameters:
        	worksheet_name (str): The name of the worksheet to update.
        	row (int): The 1-based row index of the cell.
        	col (int): The 1-based column index of the cell.
        	value: The new value to set in the specified cell.
        """
        worksheet = self.get_worksheet(worksheet_name)
        worksheet.update_cell(row, col, value)
