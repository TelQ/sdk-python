import datetime as dt
from typing import Dict, List, Union

import telq.authentication as authentication
import telq.networks as networks
import telq.results as results
from telq.tests import Test
from telq.tests import Tests
from telq.tests import BatchTests


class TelQTelecomAPI:
    """Connects to the TelQ Telecom API to perform operations such as obtaining
    a list with our available networks, send tests and consult test results.

    By default the TelQTelecomAPI uses the API Version 2.1 which can be changed
    with the API version parameter.

    NOTES
    ----------
    Please kindly be informed that this Python SDK supports API version version from 2.1 only

    Parameters
    ----------
    api_version : str, default 'v2.2'
        API version to use, defaults to version 'v2.2'
        Versions 1.0, 1.1, 1.2, 1.3 and 1.4 have been deprecated. This means no new development or bug fixes
        will occur on those versions, but they will continue to be supported
        by our app through 2021. We may stop supporting them at some point in the future
        but we will give ample warning to all our customers about it.

    Examples
    --------
    Initialise the TelQTelecomAPI class
    >>> telq_api = TelQTelecomAPI(base_url="https://api.telqtele.com")

    Authenticate the TelQ API by simply passing your App Id and App Key.
    If there are no errors, it means you have been authenticated.

    >>> telq_api.authenticate(api_id="<yourAppKey>", api_key="<yourAppId>")

    After authentication, you can get the list of available networks

    >>> telq_api.get_networks()
    [{'mcc': '350',
      'countryName': 'Bermuda',
      'mnc': '01',
      'providerName': 'Digicel',
      'portedFromMnc': None,
      'portedFromProviderName': None},
      {'mcc': '310',
      'countryName': 'United States of America',
      'mnc': '012',
      'providerName': 'Verizon',
      'portedFromMnc': '260',
      'portedFromProviderName': 'T-Mobile'},
      ...
      'mnc': '03',
      'providerName': 'Claro',
      'portedFromMnc': None,
      'portedFromProviderName': None},
      ...]

    Request New Tests

    >>> telq_api.initiate_new_tests(destinationNetworks= [{'mcc': '310',
    ...                                                   'countryName': 'United States of America',
    ...                                                   'mnc': '012',
    ...                                                   'providerName': 'Verizon',
    ...                                                   'portedFromMnc': '260',
    ...                                                   'portedFromProviderName': 'T-Mobile'}
    ...                                                 ])
    [{'id': 13754642,
      'testIdText': 'woOMJtrQAy',
      'phoneNumber': '14045183990',
      'errorMessage': None,
      'destinationNetwork': {'mcc': '310', 'mnc': '012', 'portedFromMnc': '260'},
      'testIdTextType': 'ALPHA',
      'testIdTextCase': 'MIXED',
      'testIdTextLength': 10}]

    Test Results

    >>> telq_api.get_test_results(test_id=13754642)
    {'id': 13754642,
     'testIdText': 'woOMJtrQAy',
     'senderDelivered': None,
     'textDelivered': None,
     'testCreatedAt': '2022-05-13T19:46:38.011254Z',
     'smsReceivedAt': None,
     'receiptDelay': None,
     'testStatus': 'WAIT',
     'destinationNetworkDetails': {'mcc': '310',
      'mnc': '012',
      'portedFromMnc': '260',
      'countryName': 'United States of America',
      'providerName': 'Verizon',
      'portedFromProviderName': 'T-Mobile'},
     'smscInfo': None,
     'pdusDelivered': []}
    """

    _last_time_authenticated = None

    def __init__(self, base_url: str = "https://api.telqtele.com", api_version: str = "v2.2") -> None:
        self.api_version = api_version
        self.base_url = base_url

    def authenticate(self, api_id: str, api_key: str):
        """Authenticates the App Id and Key.
        
        NOTE
        ----------
        Please note that each authentication lasts for only 24 hours, you will be required to
        authenticate every 24 hours
        
        Parameters
        ----------
        api_id : str
            TelQ uses API key pairs (appId, appKey) to allow access to the API.
            You can find your AppId and generate your AppKey on the API Menu of the TelQ App.
        api_key : str
            Your AppKey gotten from the API Menu of the TelQ App
        """ ""
        try:
            # if the user has been authenticated before
            # and its within 24 hours since the last time the user was authenticated
            if self._last_time_authenticated and (
                    dt.datetime.utcnow() -
                    self._last_time_authenticated) < dt.timedelta(days=1):
                print("Already authenticated")
            # if 24 hours has elapased
            else:
                self._authenticated = authentication.Authentication(
                    api_id=api_id, api_key=api_key, api_version=self.api_version, base_url=self.base_url
                )
                self._last_time_authenticated = dt.datetime.now()
        except AttributeError:
            # if the user has never been authenticated
            self._authenticated = authentication.Authentication(
                api_id=api_id, api_key=api_key, api_version=self.api_version, base_url=self.base_url
            )
            self._last_time_authenticated = dt.datetime.now()

    def get_networks(self) -> List[Dict[str, str]]:
        """This method retrieves a list with all our currently available Networks. 
        Please keep in mind that the list of available networks updates frequently and we recommend to retrieve the list every minute. 
        The returned values (mcc, mnc, portedFromMnc) will be used in the initiate_new_tests method to request test numbers. 
        
        - mcc is the Mobile Country Code, as defined by The ITU-T Recommendation E.212. 
        This value will always contain 3 digits.
        
        - mnc is the Mobile Network Code, as defined by The ITU-T Recommendation E.212. 
        This value can be 2 to 3 digits long.
        
        - portedFromMnc indicates from which mnc the phone number has been ported. 
        If this param is not present, the test number has not been ported and belongs to the original network.

        Returns
        -------
        List[Dict[str, str]]
            A list of currently available Networks
        """ ""
        try:
            networks_ = networks.Networks(self._authenticated)
        except AttributeError:
            raise RuntimeError(
                "You must be authenticated first - call the authenticate method passing your App Id and Key "
            )
        return networks_.get_networks()

    def initiate_new_tests(
        self,
        destinationNetworks: List[Dict[str, str]],
        resultsCallbackUrl: Union[str, None] = None,
        maxCallbackRetries: int = 3,
        testIdTextType: str = "ALPHA",
        testIdTextCase: str = "MIXED",
        testIdTextLength: int = 10,
        testTimeToLiveInSeconds: int = 3600,
    ) -> List[Dict[str, str]]:
        """This method receives a list with the Destination Networks where you want to send your tests. 
        For each requested network, a test will be created if the network is still available at the time of the test request. 

        Parameters
        ----------
        destinationNetworks : List[Dict[str, str]]
            The list of networks you want to issue tests to. This is required and cannot be empty. 
            Each network are required to have at least the mcc and mc as keys. optional are portedFromMnc
        resultsCallbackUrl : Union[str, None], optional
            The callback URL where you would like to receive TestResult updates 
            anytime your tests status changes, by default None
        maxCallbackRetries : int, optional
            The maximum number of attempts you want us to try when calling your "callback url" with updates. 
            Maximum is 5, by default 3
        testIdTextType : str, optional
            The type of testIdText to use in this test. 
            Options are: "ALPHA", "ALPHA_NUMERIC", "NUMERIC", "WHATSAPP_CODE", by default "ALPHA"
        testIdTextCase : str, optional
            The case to use for letters in the testIdText. 
            Applies only to ALPHA and ALPHA_NUMERIC types. Options are: "UPPER", "LOWER", "MIXED", by default "MIXED"
        testIdTextLength : int, optional
            The number of characters to use for generating the testIdText. default=10, minimum=4, maximum=20. 
            Doesn't apply to WHATSAPP_CODE type, since it has a fixed length of 7, by default 10
        testTimeToLiveInSeconds : int, optional
            The maximum amount of time you want your tests to wait for a message. 
            Default is 1 hour. (Minimum of 1 minute, maximum of 3 hours), by default 3600

        Returns
        -------
        JSON Response
            The Response consists of an array of Test objects, containing each a destinationNetwork 
            and details about the test request. Here is a description of each of the keys contained by a Test object:

        Raises
        ------
        Exception
            When an error occurs, the associated error is returned
        """ ""
        try:
            test_network = Tests(self._authenticated)
        except AttributeError:
            raise RuntimeError(
                "You must be authenticated first - call the authenticate method passing your App Id and Key "
            )
        return test_network.initiate_new_tests(
            destinationNetworks,
            resultsCallbackUrl,
            maxCallbackRetries,
            testIdTextType,
            testIdTextCase,
            testIdTextLength,
            testTimeToLiveInSeconds,
        )

    def initiate_new_batch_tests(
            self,
            tests: List[Test],
            resultsCallbackUrl: Union[str, None] = None,
            resultsCallbackToken: str = None,
            maxCallbackRetries: int = 1,
            dataCoding: str = "01",
            sourceTon: str = "00",
            sourceNpi: str = "12",
            testTimeToLiveInSeconds: int = 600,
            smppValidityPeriod: int = 120,
            scheduledDeliveryTime: str = None,
            replaceIfPresentFlag: int = 0,
            priorityFlag: int = 1,
            sendTextAsMessagePayloadTlv: int = 0,
            commentText: str = None,
            tlv: List[Dict[str, str]] = None,
            udh: List[Dict[str, str]] = None
    ) -> List[Dict[str, str]]:
        """Initiate a new lnt batch tests

        Parameters
        ----------
        tests : List[Test]
            List of tests in a batch. Test should be represented with Test class
        resultsCallbackUrl : Union[str, None], optional
            The callback URL where you would like to receive TestResult updates 
            anytime your tests status changes, by default None
        resultsCallbackToken : str, optional
            If you would like to authenticate our Test Results Callbacks, you can send an authentication 
            token in this parameter. It will be included as the Authorization bearer token of the callbacks 
            we make to your server.
        maxCallbackRetries : int, optional
            The maximum number of attempts you want us to try when calling your "callback url" with updates. 
            Maximum is 5, by default 1
        dataCoding : str, optional
            TODO: add description here
            Options are: 
        sourceTon : str, optional
            TODO: add description here
            Applies only to ALPHA and ALPHA_NUMERIC types. Options are: "UPPER", "LOWER", "MIXED", by default "MIXED"
        sourceNpi : int, optional
            The TON value
            Doesn't apply to WHATSAPP_CODE type, since it has a fixed length of 7, by default 10
        testTimeToLiveInSeconds : int, optional
            The maximum amount of time you want your tests to wait for a message. 
            Default is 1 hour. (Minimum of 1 minute, maximum of 3 hours), by default 3600
        smppValidityPeriod : int, optional
            TODO: add description here
            Default is 1 hour. (Minimum of 1 minute, maximum of 3 hours), by default 3600
        scheduledDeliveryTime : str, optional
            The SMPP delivery time format. It should follow the format YYMMDDhhmmsstnnp. 
            Default is 1 hour. (Minimum of 1 minute, maximum of 3 hours), by default 3600
        replaceIfPresentFlag : int, optional
            TODO: add description here
            Default is 1 hour. (Minimum of 1 minute, maximum of 3 hours), by default 3600
        priorityFlag : int, optional
            TODO: add description here
            Default is 1 hour. (Minimum of 1 minute, maximum of 3 hours), by default 3600
        sendTextAsMessagePayloadTlv : int, optional
            TODO: add description here
            Default is 1 hour. (Minimum of 1 minute, maximum of 3 hours), by default 3600
        commentText : str, optional
            The comment that can be attached to the tests
        tlv : List[Dict[str, str], optional
            Tlv value for the tests. The datatype for this type is List[Dict]. Dict should 
            contain tagHex and valueHex values.
        udh : List[Dict[str, str], optional
            Udh value for the tests. The datatype for this type is List[Dict]. Dict should 
            contain tagHex and valueHex values.

        Returns
        -------
        JSON Response
            The Response consists of an array of Test objects, containing each a destinationNetwork 
            and details about the test request. Here is a description of each of the keys contained by a Test object:

        Raises
        ------
        Exception
            When an error occurs, the associated error is returned
        """ ""
        try:
            test = BatchTests(self._authenticated)
        except AttributeError:
            raise RuntimeError(
                "You must be authenticated first - call the authenticate method passing your App Id and Key "
            )
        return test.initiate_new_tests(
            tests,
            resultsCallbackUrl,
            resultsCallbackToken,
            maxCallbackRetries,
            dataCoding,
            sourceTon,
            sourceNpi,
            testTimeToLiveInSeconds,
            smppValidityPeriod,
            scheduledDeliveryTime,
            replaceIfPresentFlag,
            priorityFlag,
            sendTextAsMessagePayloadTlv,
            commentText,
            tlv,
            udh
        )

    def get_test_results(self, test_id: int) -> Dict[str, str]:
        """Retrieve the Test Results from the id from the initiate_new_tests method

        Parameters
        ----------
        test_id : int
            id from the response of the initiate_new_tests method

        Returns
        -------
        Dict[str, str]
        """ ""
        try:
            results_ = results.Results(self._authenticated)
        except AttributeError:
            raise RuntimeError(
                "You must be authenticated first - call the authenticate method passing your App Id and Key "
            )
        return results_.get_test_results(test_id)

    def get_batch_test_results(self, date_from: str = None, date_to: str = None, page: int = 1,
                               size: int = 100, order: str = "asc"):
        """Retrieve the Test Results from the id from the initiate_new_tests method

        Parameters
        ----------
        date_from : str
            Specifies the start date and time for the range filter. ISO 8601 format
        date_to: str
            Specifies the end date and time for the range filter. ISO 8601 format
        page: int
            Specifies page for page test results
        size: int
            Specifies number of test results per page
        order: str
            Specifies order of the test results by id

        Returns
        -------
        Dict[str, str]
        """ ""
        try:
            results_ = results.Results(self._authenticated)
        except AttributeError:
            raise RuntimeError(
                "You must be authenticated first - call the authenticate method passing your App Id and Key "
            )
        return results_.get_batch_test_results(date_from, date_to, page, size, order)
