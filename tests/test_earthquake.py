import allure
from assertpy import assert_that

from session import Endpoints, RequestTypes, StatusCodes

ENDPOINT = Endpoints.EARTHQUAKE


@allure.feature('Earthquake')
@allure.story('Earthquake API')
class TestEarthquake:
    @allure.title('Test API status code')
    def test_api_status_code(self, http_object):
        status_code, _ = http_object.send_request(RequestTypes.GET, ENDPOINT)
        assert_that(status_code).is_equal_to(StatusCodes.HTTP_OK)
