import os

import pytest
import telq.authentication as authentication
from dotenv import load_dotenv

# path to the environment variables where the App Id and App Key is stored
dotenv_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "telq", ".env")
)

# load the environment variables
load_dotenv(dotenv_path)

API_ID = os.environ.get("api_id")
API_KEY = os.environ.get("api_key")


def test_invalid_api_version_1():
    with pytest.raises(ValueError):
        _ = authentication.Authentication(
            api_id=API_ID, api_key=API_KEY, api_version="3.1"
        )


def test_invalid_api_version_1():
    with pytest.raises(ValueError):
        _ = authentication.Authentication(
            api_id=API_ID, api_key=API_KEY, api_version="v2.2"
        )


def test_currently_supported_api_version_1():
    _ = authentication.Authentication(
        api_id=API_ID, api_key=API_KEY, api_version="v2.1"
    )
    assert True


def test_currently_supported_api_version_2():
    _ = authentication.Authentication(api_id=API_ID, api_key=API_KEY)
    assert True
