from todos_app.exceptions.api_exception import ApiException
from todos_app.utils.http_status_codes import HTTP_404_NOT_FOUND


class EntityNotFoundException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, HTTP_404_NOT_FOUND, "NOT_FOUND")
