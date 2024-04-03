import os
from dotenv import load_dotenv
# path to the environment variables where the App Id and App Key is stored

dotenv_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".env")
)

print("dotenv", dotenv_path)

# load the environment variables
load_dotenv(dotenv_path)

API_ID = os.environ.get("api_id", "")
API_KEY = os.environ.get("api_key", "")
BASE_URL = os.environ.get("base_url", "https://api.telqtele.com")
