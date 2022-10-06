from todos_app.exceptions.api_exception import ApiException
from todos_app.utils.http_status_codes import HTTP_409_CONFLICT


class EntityAlreadyExistException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, HTTP_409_CONFLICT, "CONFLICT")
