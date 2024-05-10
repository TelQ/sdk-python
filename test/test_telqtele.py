import pytest
from config import BASE_URL, API_ID, API_KEY
from telq import TelQTelecomAPI
from telq.session.session_data import SessionData
from telq.supplier.supplier_data import SupplierData
from telq.tests import Test


@pytest.fixture
def telq_api():
    """Initialise the TelQTelecomAPI class and authenticate the user"""
    telq_api = TelQTelecomAPI(base_url=BASE_URL)
    telq_api.authenticate(api_id=API_ID, api_key=API_KEY)
    return telq_api


def test_invalid_app_id_or_app_key():
    """Test the Token endpoint with an invalid app id or app key"""
    with pytest.raises(Exception):
        telq_api = TelQTelecomAPI(base_url=BASE_URL)
        telq_api.authenticate(api_id="invalid", api_key="invalid")


def test_token():
    """Test the Token Endpoint with the correct app credentials"""
    telq_api = TelQTelecomAPI(base_url=BASE_URL)
    telq_api.authenticate(api_id=API_ID, api_key=API_KEY)
    assert True


def test_networks_1():
    """Test the networks endpoint when the user is not authenticated"""
    telq_api = TelQTelecomAPI(base_url=BASE_URL)
    with pytest.raises(Exception):
        _ = telq_api.network.get_networks()
    assert True


def test_networks_2(telq_api: TelQTelecomAPI):
    """Test the networks endpoint"""
    _ = telq_api.network.get_networks()
    assert True


def test_tests_1(telq_api: TelQTelecomAPI):
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

    telq_api.mt.initiate_new_tests(single_network)
    assert True


def test_tests_2(telq_api: TelQTelecomAPI):
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

    telq_api.mt.initiate_new_tests(
        destinationNetworks=destinationNetworks, testIdTextCase="LOWER"
    )
    assert True


def test_tests_3(telq_api: TelQTelecomAPI):
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

    test_id = telq_api.mt.initiate_new_tests(
        destinationNetworks=destinationNetworks,
        resultsCallbackUrl="https://my-callback-url.com/telq_result",
        maxCallbackRetries=3,
        testIdTextType="NUMERIC",
        testIdTextCase="MIXED",
        testIdTextLength=7,
        testTimeToLiveInSeconds=3000,
    ).get('response')[0].get('id', 0)
    assert test_id != 0
    telq_api.mt.get_test_results(test_id)
    assert True


def test_tests_4(telq_api: TelQTelecomAPI):
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

    telq_api.mt.initiate_new_tests(
        destinationNetworks=destinationNetworks,
        testTimeToLiveInSeconds=1000,
        testIdTextCase="LOWER",
        testIdTextType="NUMERIC",
        testIdTextLength=5,
        resultsCallbackUrl="https://my-callback-url.com/telq_result",
    )
    assert True


def test_tests_5(telq_api: TelQTelecomAPI):
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
    telq_api.mt.initiate_new_tests(list_of_networks)
    assert True


def test_tests_6(telq_api: TelQTelecomAPI):
    tests = [Test(
        sender="Google",
        text="This is sample message",
        testIdTextType="ALPHA",
        testIdTextCase="LOWER",
        testIdTextLength=7,
        supplierId=6,
        mcc="276",
        mnc="02",
        portedFromMnc=None
    )]
    telq_api.lnt.initiate_new_tests(tests)


def test_tests_7(telq_api: TelQTelecomAPI):
    telq_api.lnt.get_test_results()
    assert True


def test_session_supplier_1(telq_api: TelQTelecomAPI):
    sessionData = SessionData(
        hostIp="127.0.0.1",
        hostPort=34554,
        systemId="user",
        password="pass"
    )
    res0 = telq_api.session.create(sessionData)
    res1 = telq_api.session.create(sessionData)

    sessionId0 = res0.get('smppSessionId')
    assert sessionId0 != None
    sessionId1 = res1.get('smppSessionId')
    assert sessionId1 != None
    telq_api.session.get(sessionId0)
    assert telq_api.session.list().get('content') != None
    assert len(telq_api.session.list().get('content', [])) > 0
    sessionData.smppSessionId = sessionId0
    telq_api.session.update(sessionData)

    supplierData = SupplierData(
        smppSessionId=sessionId0,
        supplierName="test supplier",
        routeType="Wholesale"
    )

    res_supplier0 = telq_api.supplier.create(supplierData)
    supplierId = res_supplier0.get('supplierId')
    assert supplierId != None
    telq_api.supplier.get(supplierId)
    assert telq_api.supplier.list().get('content') != None
    assert len(telq_api.supplier.list().get('content', [])) > 0
    supplierData.supplierId = supplierId
    telq_api.supplier.update(supplierData)

    telq_api.supplier.assign(smpp_session_id=sessionId1, supplier_id_list=[supplierId])
    assert telq_api.supplier.get(supplierId).get('smppSessionId') == sessionId1
    assert len(telq_api.supplier.list_status().get('content', [])) > 0

    telq_api.supplier.delete(supplierId)
    telq_api.session.delete(sessionId0)
    telq_api.session.delete(sessionId1)

    assert True


@pytest.mark.skip(reason="temporary disable until resolved")
def test_test_results(telq_api: TelQTelecomAPI):
    """Test the results endpoint with an id from the tests endpoint"""
    _ = telq_api.mt.get_test_results(12345678)
    assert True
