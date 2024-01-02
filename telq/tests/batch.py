from typing import Dict, List, Union

import requests
import telq.authentication as authentication
from telq.endpoints import TestsBatchURL
from telq.tests.model import Test


class BatchTests:
    """ Launch batch tests with LNT API

    Parameters
    -------
    authentication: authentication.Authentication
        The authentication class after you have been authenticated

    Raises
    ------
    Exception
        The Exception will display the error code and the message. 
        This will happen If there is an error with your request
    """ ""

    def __init__(self, authentication: authentication.Authentication):
        self._authentication = authentication

    def initiate_new_tests(
        self,
        tests: List[Test],
        resultsCallbackUrl: Union[str, None] = None,
        resultsCallbackToken: str = None,
        maxCallbackRetries: int = 1,
        dataCoding: str = "01",
        sourceTon: str = "00",
        sourceNpi: str = "12",
        testTimeToLiveInSeconds: int = 600,
        validityPeriod: int = 120,
        scheduledDeliveryTime: str = "2209131247000000",
        replaceIfPresentFlag: int = 0,
        priorityFlag: int = 1,
        sendTextAsMessagePayloadTlv: int = 0,
        commentText: str = None,
        tlv: List[Dict[str, str]] = None,
        udh: List[Dict[str, str]] = None,
    ):
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
        validityPeriod : int, optional
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
        url = TestsBatchURL(self._authentication.api_version).url()
        method = "POST"
        headers = {
            "accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": self._authentication._bearer_token
        }

        if resultsCallbackToken:
            headers["results-callback-token"] = resultsCallbackToken

        data = self._validate_parse_data(
            tests,
            resultsCallbackUrl,
            maxCallbackRetries,
            dataCoding,
            sourceTon,
            sourceNpi,
            testTimeToLiveInSeconds,
            validityPeriod,
            scheduledDeliveryTime,
            replaceIfPresentFlag,
            priorityFlag,
            sendTextAsMessagePayloadTlv,
            commentText,
            tlv,
            udh
        )
        print(data)

        response = requests.request(method, url, headers=headers, json=data)

        res = response.json()
        try:
            if 'error' in res:
                err = res['message'] if 'message' in res else res['error']
                raise ValueError(err)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise e
        return res

    def _validate_parse_data(
        self,
        tests: List[Test],
        resultsCallbackUrl: Union[str, None],
        maxCallbackRetries: int,
        dataCoding: str,
        sourceTon: str,
        sourceNpi: str,
        testTimeToLiveInSeconds: int,
        validityPeriod: int,
        scheduledDeliveryTime: str,
        replaceIfPresentFlag: int,
        priorityFlag: int,
        sendTextAsMessagePayloadTlv: int,
        commentText: str,
        tlv: List[Dict[str, str]],
        udh: List[Dict[str, str]]
    ) -> Dict[str, str]:
        if len(tests) == 0:
            raise KeyError(
                "at least one test should be supplied in the tests parameter"
            )

        for test in tests:
            if not isinstance(test, Test):
                raise KeyError(
                    "test should be instance of Test class"
                )

        data = {
            "tests": [test.__dict__ for test in tests],
            "resultsCallbackUrl": resultsCallbackUrl,
            "maxCallbackRetries": maxCallbackRetries,
            "dataCoding": dataCoding,
            "sourceTon": sourceTon,
            "sourceNpi": sourceNpi,
            "testTimeToLiveInSeconds": testTimeToLiveInSeconds,
            "validityPeriod": validityPeriod,
            "scheduledDeliveryTime": scheduledDeliveryTime,
            "replaceIfPresentFlag": replaceIfPresentFlag,
            "priorityFlag": priorityFlag,
            "sendTextAsMessagePayloadTlv": sendTextAsMessagePayloadTlv,
            "commentText": commentText,
            "tlv": tlv,
            "udh": udh
        }
        return data
