""" Test the generated URL that it gives the expected URL regardless of the API version specified"""

from config import BASE_URL
import telq.endpoints as endpoints

DEFAULT_API_VERSION = "v3"

def test_token_url_1():
    actual = endpoints.TokenURL(base_url=BASE_URL).url()
    expected = f"{BASE_URL}/{DEFAULT_API_VERSION}/client/token"
    message = f"API version {DEFAULT_API_VERSION} Token endpoint received {actual} instead of {expected}"
    assert actual == expected, message


def test_token_url_2():
    actual = endpoints.TokenURL(base_url=BASE_URL, api_version="v1.5").url()
    expected = f"{BASE_URL}/v1.5/client/token"
    message = f"API version v1.5 Token endpoint received {actual} instead of {expected}"
    assert actual == expected, message


def test_networks_url_1():
    actual = endpoints.NetworksURL(base_url=BASE_URL).url()
    expected = f"{BASE_URL}/{DEFAULT_API_VERSION}/client/networks"
    message = (
        f"API version {DEFAULT_API_VERSION} networks endpoint received {actual} instead of {expected}"
    )
    assert actual == expected, message


def test_networks_url_2():
    actual = endpoints.NetworksURL(base_url=BASE_URL, api_version="v1.5").url()
    expected = f"{BASE_URL}/v1.5/client/networks"
    message = (
        f"API version v1.5 networks endpoint received {actual} instead of {expected}"
    )
    assert actual == expected, message


def test_tests_url_1():
    actual = endpoints.TestsURL(base_url=BASE_URL).url()
    expected = f"{BASE_URL}/{DEFAULT_API_VERSION}/client/tests"
    message = f"API version {DEFAULT_API_VERSION} endpoint received {actual} instead of {expected}"
    assert actual == expected, message


def test_tests_url_2():
    actual = endpoints.TestsURL(base_url=BASE_URL, api_version="v1.5").url()
    expected = f"{BASE_URL}/v1.5/client/tests"
    message = f"API version v1.5 tests endpoint received {actual} instead of {expected}"
    assert actual == expected, message


def test_results_url_1():
    actual = endpoints.ResultsURL(base_url=BASE_URL).url(test_id=5)
    expected = f"{BASE_URL}/{DEFAULT_API_VERSION}/client/tests/5"
    message = (
        f"API version {DEFAULT_API_VERSION} results endpoint received {actual} instead of {expected}"
    )
    assert actual == expected, message


def test_results_url_2():
    actual = endpoints.ResultsURL(base_url=BASE_URL, api_version="v1.5").url(test_id=908)
    expected = f"{BASE_URL}/v1.5/client/tests/908"
    message = (
        f"API version v1.5 results endpoint received {actual} instead of {expected}"
    )
    assert actual == expected, message


def test_session_url_1():
    actual = endpoints.SessionItemURL(base_url=BASE_URL).url(id=908)
    expected = f"{BASE_URL}/{DEFAULT_API_VERSION}/client/sessions/908"
    message = (
        f"API version {DEFAULT_API_VERSION} results endpoint received {actual} instead of {expected}"
    )
    assert actual == expected, message


def test_session_url_2():
    actual = endpoints.SessionURL(base_url=BASE_URL).url()
    expected = f"{BASE_URL}/{DEFAULT_API_VERSION}/client/sessions"
    message = (
        f"API version {DEFAULT_API_VERSION} results endpoint received {actual} instead of {expected}"
    )
    assert actual == expected, message
