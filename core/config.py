import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chromium")

    # UI base URLs
    SAUCE_URL = os.getenv("SAUCE_URL", "https://www.saucedemo.com")
    DEMOQA_URL = os.getenv("DEMOQA_URL", "https://demoqa.com")

    # Auth / test users
    SAUCE_USERNAME = os.getenv("SAUCE_USERNAME", "standard_user")
    SAUCE_PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")

    # API base URLs
    REQRES_URL = os.getenv("REQRES_URL", "https://reqres.in/api")
