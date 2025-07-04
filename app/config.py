import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """Base configuration class."""
    SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT_PATH")

    

