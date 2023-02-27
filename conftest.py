import pytest
import allure

from session import HTTPSession


@allure.step('Making request to {endpoint}')
@pytest.fixture(scope='class', autouse=True)
def http_object():
    http_object = HTTPSession()
    return http_object
