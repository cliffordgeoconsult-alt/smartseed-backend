# app/core/gee_auth.py
import ee
import os
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

def init_gee() -> None:
    """
    Initialize Google Earth Engine using a service account.
    This must run once at app startup.
    """

    service_account_email = os.getenv("GEE_SERVICE_ACCOUNT")
    key_path = os.getenv("GEE_PRIVATE_KEY_PATH")

    if not service_account_email or not key_path:
        raise RuntimeError("GEE environment variables are missing")

    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes=["https://www.googleapis.com/auth/earthengine"]
    )

    ee.Initialize(credentials)
    print("Google Earth Engine initialized successfully")
