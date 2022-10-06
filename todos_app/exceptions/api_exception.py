class ApiException(Exception):
    def __init__(self, message: str, http_status_code, http_status):
        self.message = message
        self.http_status_code = http_status_code
        self.http_status = http_status
        super().__init__(message, http_status, http_status_code)

    def to_dict(self):
        return {
            'message': self.message
        }