import os

import pytest
from dotenv import load_dotenv
from telq import TelQTelecomAPI

# path to the environment variables where the App Id and App Key is stored
dotenv_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "telq", ".env")
)

# load the environment variables
load_dotenv(dotenv_path)

API_ID = os.environ.get("api_id")
API_KEY = os.environ.get("api_key")


@pytest.fixture
def telq_api():
    """Initialise the TelQTelecomAPI class and authenticate the user"""
    telq_api = TelQTelecomAPI()
    telq_api.authenticate(api_id=API_ID, api_key=API_KEY)
    return telq_api


def test_invalid_app_id_or_app_key():
    """Test the Token endpoint with an invalid app id or app key"""
    with pytest.raises(Exception):
        _ = TelQTelecomAPI(api_id="invalid-id", api_key="invalid-key")


def test_token():
    """Test the Token Endpoint with the correct app credentials"""
    telq_api = TelQTelecomAPI()
    telq_api.authenticate(api_id=API_ID, api_key=API_KEY)
    assert True


def test_networks_1():
    """Test the networks endpoint when the user is not authenticated"""
    telq_api = TelQTelecomAPI()
    with pytest.raises(RuntimeError):
        _ = telq_api.get_networks()
    assert True


def test_networks_2(telq_api):
    """Test the networks endpoint"""
    _ = telq_api.get_networks()
    assert True


def test_tests_1(telq_api):
    """Test the tests endpoint with a single network"""
    single_network = [
        {
            "mcc": "246",
            "countryName": "Lithuania",
            "mnc": "03",
            "providerName": "Tele2",
            "portedFromMnc": "02",
            "portedFromProviderName": "BITE",
        }
    ]

    telq_api.initiate_new_tests(single_network)
    assert True


def test_tests_2(telq_api):
    """Test the tests endpoint with optional parameters"""
    destinationNetworks = [
        {
            "mcc": "246",
            "countryName": "Lithuania",
            "mnc": "03",
            "providerName": "Tele2",
            "portedFromMnc": "02",
            "portedFromProviderName": "BITE",
        }
    ]

    telq_api.initiate_new_tests(
        destinationNetworks=destinationNetworks, testIdTextCase="LOWER"
    )
    assert True


def test_tests_3(telq_api):
    """Test the tests endpoint with other optional parameters"""
    destinationNetworks = [
        {
            "mcc": "246",
            "countryName": "Lithuania",
            "mnc": "03",
            "providerName": "Tele2",
            "portedFromMnc": "02",
            "portedFromProviderName": "BITE",
        }
    ]

    telq_api.initiate_new_tests(
        destinationNetworks=destinationNetworks,
        resultsCallbackUrl="https://my-callback-url.com/telq_result",
        maxCallbackRetries=3,
        testIdTextType="NUMERIC",
        testIdTextCase="MIXED",
        testIdTextLength=7,
        testTimeToLiveInSeconds=3000,
    )
    assert True


def test_tests_4(telq_api):
    """Test the tests endpoint with other optional parameters"""
    destinationNetworks = [
        {
            "mcc": "246",
            "countryName": "Lithuania",
            "mnc": "03",
            "providerName": "Tele2",
            "portedFromMnc": "02",
            "portedFromProviderName": "BITE",
        }
    ]

    telq_api.initiate_new_tests(
        destinationNetworks=destinationNetworks,
        testTimeToLiveInSeconds=1000,
        testIdTextCase="LOWER",
        testIdTextType="NUMERIC",
        testIdTextLength=5,
        resultsCallbackUrl="https://my-callback-url.com/telq_result",
    )
    assert True


def test_tests_5(telq_api):
    """Test the tests endpoint with a list of networks"""
    list_of_networks = [
        {
            "mcc": "246",
            "countryName": "Lithuania",
            "mnc": "03",
            "providerName": "Tele2",
            "portedFromMnc": "02",
            "portedFromProviderName": "BITE",
        },
        {
            "mcc": "364",
            "countryName": "Bahamas",
            "mnc": "49",
            "providerName": "Aliv",
            "portedFromMnc": None,
            "portedFromProviderName": None,
        },
        {
            "mcc": "724",
            "countryName": "Brazil",
            "mnc": "00",
            "providerName": "Nextel",
            "portedFromMnc": None,
            "portedFromProviderName": None,
        },
    ]
    telq_api.initiate_new_tests(list_of_networks)
    assert True


def test_test_results(telq_api):
    """Test the results endpoint with an id from the tests endpoint"""
    _ = telq_api.get_test_results(12345678)
    assert True
