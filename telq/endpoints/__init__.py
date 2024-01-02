from abc import ABC, abstractmethod


class TelQURL(ABC):
    """Base class for generating TelQ URLs for the endpoints. This class sets the stage for each endpoint URL 
    
    Attributes
    ----------
    schemes : str
        https
    host : str
        api.telqtele.com

    Parameters
    ----------
    api_version : str
        API version, for example: 'v1.5', defaults to 'v2.2'
    """ ""

    schemes = "https"
    host = "api.telqtele.com"

    def __init__(self, api_version: str = "v2.2"):
        self.base_path = f"/{api_version}/client"

    def create_base_url(self):
        return TelQURL.schemes + "://" + TelQURL.host + self.base_path

    @abstractmethod
    def path(**kwargs) -> str:
        raise NotImplementedError

    def url(self, **kwargs):
        return self.create_base_url() + self.path(**kwargs)


class TokenURL(TelQURL):
    """Endpoint for Token authentication"""

    def path(self) -> str:
        return "/token"


class NetworksURL(TelQURL):
    """Endpoint for networks"""

    def path(self) -> str:
        return "/networks"


class TestsURL(TelQURL):
    """Endpoint for tests"""

    def path(self) -> str:
        return "/tests"

class TestsBatchURL(TelQURL):
    """Endpoint for tests"""

    def path(self) -> str:
        return "/lnt/tests"


class ResultsURL(TelQURL):
    """Endpoint for results"""

    def path(self, id) -> str:
        return f"/results/{id}"
