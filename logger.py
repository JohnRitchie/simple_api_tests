# fork from https://github.com/ashrika786/api-testing-python

from datetime import datetime


class Logger(object):
    @classmethod
    def write_to_file(cls, events):
        current_date = datetime.now()

        with open('output.log', 'a', encoding='utf-8') as file:
            for event_text in events:
                file.write(f'{current_date}  {event_text}\n')

    @classmethod
    def log(cls, events):
        cls.write_to_file(events)

    @classmethod
    def log_request(cls, request_type, url, params, response_status_code):
        events = [
            f'Executed {request_type.__name__.upper()} request',
            f'URL: {url}',
            f'PARAMETERS: {params}',
            f'RESPONSE STATUS CODE: {response_status_code}'
        ]
        cls.log(events)
