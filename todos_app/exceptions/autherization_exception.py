from todos_app.exceptions.api_exception import ApiException
from todos_app.utils.http_status_codes import HTTP_401_UNAUTHORIZED


class AuthorizationException(ApiException):
    def __init__(self):
        super().__init__('شما دسترسی لازم برای این درخواست را ندارید', HTTP_401_UNAUTHORIZED, 'UNAUTHORIZED')