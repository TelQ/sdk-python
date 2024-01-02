from typing import Dict, List, Union

import requests
import telq.authentication as authentication
from telq.endpoints import TestsURL


class Tests:
    """Receives a list with the Destination Networks where you want to send your tests. 
    For each requested network, a test will be created if the network is still available 
    at the time of the test request. 
    Keep in mind that networks can go offline sometimes after the results 
    from the /networks endpoint have been returned.

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
        destinationNetworks: List[Dict[str, str]],
        resultsCallbackUrl: Union[str, None] = None,
        maxCallbackRetries: int = 3,
        testIdTextType: str = "ALPHA",
        testIdTextCase: str = "MIXED",
        testIdTextLength: int = 10,
        testTimeToLiveInSeconds: int = 3600,
    ):
        """Initiate a new test

        Parameters
        ----------
        destinationNetworks : List[Dict[str, str]]
            The list of networks you want to issue tests to. This is required and cannot be empty. 
            Each network are required to have at least the mcc and mc as keys. optional are portedFromMnc
        resultsCallbackUrl : Union[str, None], optional
            The callback URL where you would like to receive TestResult updates 
            anytime your tests status changes, by default None
        maxCallbackRetries : int, optional
            The maximum number of attemps you want us to try when calling your "callback url" with updates. 
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
        url = TestsURL(self._authentication.api_version).url()
        method = "POST"
        headers = {
            "accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": self._authentication._bearer_token,
        }

        data = self._validate_parse_data(
            destinationNetworks,
            resultsCallbackUrl,
            maxCallbackRetries,
            testIdTextType,
            testIdTextCase,
            testIdTextLength,
            testTimeToLiveInSeconds,
        )

        response = requests.request(method, url, headers=headers, json=data)

        res = response.json()
        try:
            if 'error' in res:
                raise ValueError(res['message'])
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise (e)
        return res

    def _validate_parse_data(
        self,
        destinationNetworks: List[Dict[str, str]],
        resultsCallbackUrl: Union[str, None],
        maxCallbackRetries,
        testIdTextType,
        testIdTextCase,
        testIdTextLength,
        testTimeToLiveInSeconds: int,
    ) -> Dict[str, str]:
        if not isinstance(destinationNetworks, list):
            raise ValueError(
                "destinationNetworks is a list of networks you want to issue tests to, ensure its a list"
            )
        for network in destinationNetworks:
            print(network)
            if not {"mcc", "mnc"}.issubset(network) and not {"phoneNumber"}.issubset(network):
                raise KeyError(
                    "destinationNetworks is missing one or two required parameters ('mcc' or 'mnc') or 'phoneNumber'"
                )

        data = {
            "destinationNetworks": destinationNetworks,
            "resultsCallbackUrl": resultsCallbackUrl,
            "maxCallbackRetries": maxCallbackRetries,
            "testIdTextType": testIdTextType,
            "testIdTextCase": testIdTextCase,
            "testIdTextLength": testIdTextLength,
            "testTimeToLiveInSeconds": testTimeToLiveInSeconds,
        }
        return data
