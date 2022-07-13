import requests
import telq.authentication as authentication
from telq.endpoints import ResultsURL


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

    def get_test_results(self, id: int):
        url = ResultsURL(self._authentication.api_version).url(id=id)
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
