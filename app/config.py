import os
from dotenv import load_dotenv


load_dotenv()

 class Config:
     """Base configuration class."""
     SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT_PATH")
 
     @classmethod
     def validate(cls):
         """Validate required configuration values."""
         if not cls.SERVICE_ACCOUNT:
             raise ValueError("SERVICE_ACCOUNT_PATH environment variable is required")
         if not os.path.exists(cls.SERVICE_ACCOUNT):
             raise ValueError(f"Service account file not found: {cls.SERVICE_ACCOUNT}")

    

