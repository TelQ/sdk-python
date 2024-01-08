import requests
import telq.authentication as authentication
from telq.endpoints import ResultsURL
from telq.endpoints import BatchResultsURL


class Results:
    """Sends request to the results endpoint with an id received from the tests endpoint

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

    def get_test_results(self, test_id: int):
        url = ResultsURL(self._authentication.base_url, self._authentication.api_version).url(test_id=test_id)
        method = "GET"
        headers = {
            "accept": "*/*",
            "Authorization": self._authentication._bearer_token,
        }
        response = requests.request(method, url, headers=headers)

        res = response.json()
        try:
            if 'error' in res:
                raise ValueError(res['message'])
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(e)
        return res

    def get_batch_test_results(self, date_from: str, date_to: str, page: int = 1, size: int = 100, order: str = "asc"):
        url = (BatchResultsURL(self._authentication.base_url, self._authentication.api_version)
               .url(date_from, date_to, page, size, order))
        print(url)
        method = "GET"
        headers = {
            "accept": "*/*",
            "Authorization": self._authentication._bearer_token,
        }
        response = requests.request(method, url, headers=headers)

        if response.status_code != 200:
            raise ValueError("Got HTTP status code " + str(response.status_code))

        res = response.json()
        try:
            if 'error' in res and res['error'] is not None:
                raise ValueError(res['message'])
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(e)
        return res
