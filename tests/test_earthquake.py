import pytest
import allure
from assertpy import assert_that

from session import Endpoints, RequestTypes, StatusCodes

ENDPOINT = Endpoints.EARTHQUAKE
DATA_STRUCTURE = ['timestamp', 'latitude', 'longitude', 'depth', 'size', 'quality', 'humanReadableLocation']
DATA_TYPE = [str, float, float, (float, int), (float, int), float, str]


@allure.feature('Earthquake')
@allure.story('Earthquake API')
class TestEarthquake:
    @allure.title('Test API status code')
    def test_api_status_code(self, http_object):
        status_code, _ = http_object.send_request(RequestTypes.GET, ENDPOINT)
        assert_that(status_code).is_equal_to(StatusCodes.HTTP_OK)

    @allure.title('Test API data structure')
    def test_data_structure(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(type(data)).is_equal_to(dict)
        assert_that('results' in data.keys()).is_true()
        assert_that(all([isinstance(record, dict) for record in data['results']])).is_true()

        for key in DATA_STRUCTURE:
            assert_that(all(key in record.keys() for record in data['results'])).is_true()

        for record in data['results']:
            assert_that(all(key in DATA_STRUCTURE for key in record.keys())).is_true()

    @allure.title('Test API data type')
    @pytest.mark.parametrize(
        'entity, entity_type', list(zip(DATA_STRUCTURE, DATA_TYPE))
    )
    def test_data_type(self, http_object, entity, entity_type):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([isinstance(record[entity], entity_type) for record in data['results']])).is_true()
