# fork from https://github.com/ashrika786/api-testing-python

import json
from requests import RequestException, Session
import allure

from logger import Logger


class HTTPSession(Session):
    @staticmethod
    @allure.step('Making request to {endpoint}')
    def send_request(request_type, endpoint, **params):
        try:
            response = request_type(endpoint, **params)
            Logger.log_request(request_type, endpoint, params, response.status_code)
            return response.status_code, json.loads(response.text)
        except RequestException as e:
            Logger.log('Could not send {} request due to exception: {}'.format(request_type, e))


class RequestTypes(object):
    GET = HTTPSession().get


class Endpoints(object):
    BASE_URL = 'http://apis.is/'
    EARTHQUAKE = BASE_URL + 'earthquake/is'


class StatusCodes(object):
    HTTP_OK = 200
    