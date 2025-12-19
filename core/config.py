import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chromium")
    SAUCE_USERNAME = os.getenv("SAUCE_USERNAME", "standard_user")
    SAUCE_PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")
    REQRES_URL = "https://reqres.in"
