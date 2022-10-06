from todos_app.exceptions.api_exception import ApiException
from todos_app.utils.http_status_codes import HTTP_400_BAD_REQUEST


class InvalidRequestException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, HTTP_400_BAD_REQUEST, "INVALID_REQUEST")