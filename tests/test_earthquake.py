import pytest
import allure
from assertpy import assert_that
from datetime import datetime
import re

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

    @allure.title('Test timestamp format')
    def test_timestamp_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([isinstance(datetime.strptime(record['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ'), datetime)
                         for record in data['results']])).is_true()

    @allure.title('Test latitude format')
    def test_latitude_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([62 < record['latitude'] < 67 for record in data['results']])).is_true()

    @allure.title('Test longitude format')
    def test_longitude_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([-30 < record['longitude'] < -11 for record in data['results']])).is_true()

    @allure.title('Test depth format')
    def test_depth_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([0 < record['depth'] < 800 for record in data['results']])).is_true()

    @allure.title('Test size format')
    @pytest.mark.xfail(reason="The data contains a negative size")
    def test_size_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([0 < record['size'] < 9 for record in data['results']])).is_true()

    @allure.title('Test quality format')
    def test_quality_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([0 < record['quality'] < 100 for record in data['results']])).is_true()

    @allure.title('Test humanReadableLocation format')
    def test_humanReadableLocation_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([re.match(r'^\d+,\d+ km [A|S|N|V]{1,3} af .*$', record['humanReadableLocation']) is not None
                         for record in data['results']])).is_true()
