import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """Base configuration class."""
    SHEET_LINK = os.getenv("SHEET_LINK")
    TYPE = os.getenv("TYPE")
    PROJECT_ID = os.getenv("PROJECT_ID")
    PRIVATE_KEY_ID = os.getenv("PRIVATE_KEY_ID")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY").replace('\\n', '\n') if os.getenv("PRIVATE_KEY") else None
    CLIENT_EMAIL = os.getenv("CLIENT_EMAIL")
    CLIENT_ID = os.getenv("CLIENT_ID")
    AUTH_URI = os.getenv("AUTH_URI")
    TOKEN_URI = os.getenv("TOKEN_URI")
    AUTH_PROVIDER_X509_CERT_URL = os.getenv("AUTH_PROVIDER_X509_CERT_URL")
    CLIENT_X509_CERT_URL = os.getenv("CLIENT_X509_CERT_URL")
    UNIVERSE_DOMAIN = os.getenv("UNIVERSE_DOMAIN")


    @classmethod
    def get_service_account(cls):
        """
        Returns the service account credentials as a dictionary.
        """
        return {
            "type": cls.TYPE,
            "project_id": cls.PROJECT_ID,
            "private_key_id": cls.PRIVATE_KEY_ID,
            "private_key": cls.PRIVATE_KEY,
            "client_email": cls.CLIENT_EMAIL,
            "client_id": cls.CLIENT_ID,
            "auth_uri": cls.AUTH_URI,
            "token_uri": cls.TOKEN_URI,
            "auth_provider_x509_cert_url": cls.AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": cls.CLIENT_X509_CERT_URL
        }
    
 
    @classmethod
    def validate(cls):
        """Validate required configuration values."""
        SERVICE_ACCOUNT = cls.get_service_account()
        if not SERVICE_ACCOUNT:
            raise ValueError("SERVICE_ACCOUNT_PATH environment variable is required")
       
    

