import pytest
import allure
from assertpy import assert_that
from datetime import datetime
import re

from session import Endpoints, RequestTypes, StatusCodes

ENDPOINT = Endpoints.EARTHQUAKE
DATA_STRUCTURE = ['timestamp', 'latitude', 'longitude', 'depth', 'size', 'quality', 'humanReadableLocation']
DATA_TYPE = [str, float, float, (float, int), (float, int), float, str]

# Icelandic coordinates only
MIN_LATITUDE = 62
MAX_LATITUDE = 67
MIN_LONGITUDE = -30
MAX_LONGITUDE = -11

# Known ranges of earthquake characteristics
MIN_DEPTH = 0
MAX_DEPTH = 800
MIN_SIZE = 0
MAX_SIZE = 9
MIN_QUALITY = 0
MAX_QUALITY = 100


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

        assert_that(all([MIN_LATITUDE < record['latitude'] < MAX_LATITUDE for record in data['results']])).is_true()

    @allure.title('Test longitude format')
    def test_longitude_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([MIN_LONGITUDE < record['longitude'] < MAX_LONGITUDE for record in data['results']])).is_true()

    @allure.title('Test depth format')
    def test_depth_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([MIN_DEPTH < record['depth'] < MAX_DEPTH for record in data['results']])).is_true()

    @allure.title('Test size format')
    @pytest.mark.xfail(reason="The data contains a negative size")
    def test_size_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([MIN_SIZE < record['size'] < MAX_SIZE for record in data['results']])).is_true()

    @allure.title('Test quality format')
    def test_quality_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([MIN_QUALITY < record['quality'] < MAX_QUALITY for record in data['results']])).is_true()

    @allure.title('Test humanReadableLocation format')
    def test_humanReadableLocation_format(self, http_object):
        _, data = http_object.send_request(RequestTypes.GET, ENDPOINT)

        assert_that(all([re.match(r'^\d+,\d+ km [A|S|N|V]{1,3} af .*$', record['humanReadableLocation']) is not None
                         for record in data['results']])).is_true()
