import os
from dotenv import load_dotenv


load_dotenv()

class Config:
     """Base configuration class."""
     SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT_PATH")
     SHEET_LINK = os.getenv("SHEET_LINK")
 
     @classmethod
     def validate(cls):
         """
         Checks that the service account path is set and the corresponding file exists.
         
         Raises:
             ValueError: If the SERVICE_ACCOUNT_PATH environment variable is missing or the specified file does not exist.
         """
         if not cls.SERVICE_ACCOUNT:
             raise ValueError("SERVICE_ACCOUNT_PATH environment variable is required")
         if not os.path.exists(cls.SERVICE_ACCOUNT):
             raise ValueError(f"Service account file not found: {cls.SERVICE_ACCOUNT}")

    

