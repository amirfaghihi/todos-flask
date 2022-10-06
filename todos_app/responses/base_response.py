from datetime import datetime


class BaseResponse:
    def __init__(self,
                 http_status_code: int,
                 http_status: str,
                 data: dict,
                 error: dict = None):
        self.error = {} if error is None else error
        self.http_status_code = http_status_code
        self.http_status = http_status
        self.data = data
        self.timestamp = datetime.now()

    def to_dict(self):
        return {'http_status_code': self.http_status_code,
                'http_status': self.http_status,
                'data': self.data,
                'error': self.error,
                'timestamp': self.timestamp}
