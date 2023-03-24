from datetime import datetime


class Logger:
    @staticmethod
    def write_events_to_file(events, file_name):
        current_date = datetime.now()

        try:
            with open(file_name, 'a', encoding='utf-8') as file:
                for event_text in events:
                    file.write(f'{current_date}  {event_text}\n')
        except Exception as e:
            print(f'Error writing to file: {e}')

    @classmethod
    def log(cls, events, file_name='output.log'):
        cls.write_events_to_file(events, file_name)

    @classmethod
    def log_http_request(cls, method, url_address, request_params, status_code, file_name='output.log'):
        events = [
            f'Executed {method.upper()} request',
            f'URL: {url_address}',
            f'REQUEST PARAMETERS: {request_params}',
            f'STATUS CODE: {status_code}'
        ]

        try:
            cls.log(events, file_name)
        except Exception as e:
            print(f'Error logging HTTP request: {e}')
