from abc import ABC, abstractmethod
from urllib.parse import urljoin
from urllib.parse import urlencode


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
    base_url = "https://api.telqtele.com"

    def __init__(self, base_url: str = "https://api.telqtele.com", api_version: str = "v2.2"):
        self.base_url = base_url
        self.base_path = f"/{api_version}/client"

    def create_base_url(self):
        return self.base_url + self.base_path

    @abstractmethod
    def path(self, **kwargs) -> str:
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

    def path(self, test_id) -> str:
        return f"/results/{test_id}"


class BatchResultsURL(TelQURL):
    """Endpoint for batch results"""
    def url(self, date_from: str, date_to: str, page: int = 1, size: int = 100, order: str = "asc") -> str:
        query_params = {
            "page": page,
            "size": size,
            "order": order
        }
        if date_from is not None:
            query_params["from"] = date_from
        if date_to is not None:
            query_params["to"] = date_to
        return urljoin(self.create_base_url() + self.path(), "?" + urlencode(query_params))

    def path(self) -> str:
        return f"/lnt/tests"
