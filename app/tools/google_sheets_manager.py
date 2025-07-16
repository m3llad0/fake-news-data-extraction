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
        Initializes the GoogleSheetsManager with service account credentials and opens a Google Spreadsheet by its URL.
        
        Parameters:
        	spreadsheet_name (str, optional): The URL of the Google Spreadsheet to open.
        
        Raises:
        	ValueError: If the service account path is missing in the configuration or if the spreadsheet cannot be opened.
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
        Retrieves a worksheet by name from the opened spreadsheet, creating it with default size if it does not exist.
        
        If the worksheet does not exist, a new worksheet with 100 rows and 20 columns is created and returned.
        
        Parameters:
            worksheet_name (str): Name of the worksheet to retrieve or create.
        
        Returns:
            Worksheet: The existing or newly created worksheet object.
        
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
        Retrieve all rows from the specified worksheet as a list of dictionaries, with each dictionary mapping column headers to cell values.
        
        Parameters:
            worksheet_name (str): Name of the worksheet to retrieve data from.
        
        Returns:
            List[Dict[str, Any]]: List of row dictionaries keyed by column headers.
        """
        worksheet = self.get_worksheet(worksheet_name)
        return worksheet.get_all_records()

    def append_row(self, worksheet_name, row_data):
        """
        Appends a new row of cell values to the specified worksheet.
        
        Parameters:
            worksheet_name (str): Name of the worksheet to append the row to.
            row_data (list): List of values representing the new row to add.
        """
        worksheet = self.get_worksheet(worksheet_name)
        worksheet.append_row(row_data)

    def update_row(self, worksheet_name, row, col, value):
        """
        Update the value of a specific cell in the given worksheet.
        
        Parameters:
        	worksheet_name (str): Name of the worksheet to update.
        	row (int): 1-based row index of the cell to update.
        	col (int): 1-based column index of the cell to update.
        	value: New value to set in the specified cell.
        """
        worksheet = self.get_worksheet(worksheet_name)
        worksheet.update_cell(row, col, value)
