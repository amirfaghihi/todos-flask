from todos_app.exceptions.api_exception import ApiException
from todos_app.utils.http_status_codes import HTTP_401_UNAUTHORIZED


class AuthenticationException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, HTTP_401_UNAUTHORIZED, "Could not verify")