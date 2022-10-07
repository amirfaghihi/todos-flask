from functools import wraps

from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request

from todos_app.exceptions.autherization_exception import AuthorizationException


def role_required(required_roles: list):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims['role']
            if not role:
                raise AuthorizationException()
            for required_role in required_roles:
                if required_role == role:
                    return fn(*args, **kwargs)

            raise AuthorizationException()

        return decorator

    return wrapper
