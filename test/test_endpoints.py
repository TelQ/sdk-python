""" Test the generated URL that it gives the expected URL regardless of the API version specified"""

import telq.endpoints as endpoints


def test_token_url_1():
    actual = endpoints.TokenURL().url()
    expected = "https://api.telqtele.com/v2.1/client/token"
    message = f"API version v2.1 Token endpoint received {actual} instead of {expected}"
    assert actual == expected, message


def test_token_url_2():
    actual = endpoints.TokenURL(api_version="v1.5").url()
    expected = "https://api.telqtele.com/v1.5/client/token"
    message = f"API version v1.5 Token endpoint received {actual} instead of {expected}"
    assert actual == expected, message


def test_networks_url_1():
    actual = endpoints.NetworksURL().url()
    expected = "https://api.telqtele.com/v2.1/client/networks"
    message = (
        f"API version v2.1 networks endpoint received {actual} instead of {expected}"
    )
    assert actual == expected, message


def test_networks_url_2():
    actual = endpoints.NetworksURL(api_version="v1.5").url()
    expected = "https://api.telqtele.com/v1.5/client/networks"
    message = (
        f"API version v1.5 networks endpoint received {actual} instead of {expected}"
    )
    assert actual == expected, message


def test_tests_url_1():
    actual = endpoints.TestsURL().url()
    expected = "https://api.telqtele.com/v2.1/client/tests"
    message = f"API version v2.1 tests endpoint received {actual} instead of {expected}"
    assert actual == expected, message


def test_tests_url_2():
    actual = endpoints.TestsURL(api_version="v1.5").url()
    expected = "https://api.telqtele.com/v1.5/client/tests"
    message = f"API version v1.5 tests endpoint received {actual} instead of {expected}"
    assert actual == expected, message


def test_results_url_1():
    actual = endpoints.ResultsURL().url(id=5)
    expected = "https://api.telqtele.com/v2.1/client/results/5"
    message = (
        f"API version v2.1 results endpoint received {actual} instead of {expected}"
    )
    assert actual == expected, message


def test_results_url_2():
    actual = endpoints.ResultsURL(api_version="v1.5").url(id=908)
    expected = "https://api.telqtele.com/v1.5/client/results/908"
    message = (
        f"API version v1.5 results endpoint received {actual} instead of {expected}"
    )
    assert actual == expected, message
