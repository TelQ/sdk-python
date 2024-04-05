from abc import ABC
import os
import requests
import toml
from typing import Optional

from requests.exceptions import JSONDecodeError

from telq.authentication import Authentication

class TelQRest(ABC):
    def __init__(self, authentcation: Optional[Authentication] = None):
        self._authentication = authentcation
        self.sdk_version = self.__get_sdk_version__()

    def __get_sdk_version__(self):
        pyproject_toml_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "pyproject.toml")
        )
        with open(pyproject_toml_path, "r") as file:
            content = file.read()

        # Parse the content using the toml library
        data = toml.loads(content)

        # Extract the version (assuming it's under [tool.poetry])
        version = data["tool"]["poetry"]["version"]
        return version

    def request(self, url: str, method: str, data: Optional[dict] = None, extra_headers: Optional[dict] = None) -> dict:
        headers = {
            "accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": f"python-sdk/{self.sdk_version}"
        }
        if self._authentication:
            headers["Authorization"] = self._authentication._bearer_token
        if extra_headers:
            headers.update(extra_headers)

        response = requests.request(method, url, headers=headers, json=data)

        try:
            res = response.json()
        except JSONDecodeError:
            res = response.text

        try:
            if isinstance(res, dict) and res.get('error') != None:
                raise ValueError(f"Server returned {url} HTTP {response.status_code}: {res}")
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise (e)

        return res if isinstance(res, dict) else {"response": res}
