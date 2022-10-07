from flask import Blueprint, request

from todos_app.models.role import Role
from todos_app.repositories.user_repo import add_user
from todos_app.exceptions.entity_already_exist_exception import EntityAlreadyExistException
from todos_app.models import User
from todos_app.repositories import user_repo

from todos_app.exceptions.authentication_exception import AuthenticationException
from todos_app.exceptions.invalid_request_exception import InvalidRequestException
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user

from todos_app.schemas.user_schema import user_schema
from todos_app.utils.http_status_codes import HTTP_200_OK

auth_blueprint = Blueprint(name='auth_blueprint', import_name=__name__, url_prefix='/v1/auth')


@auth_blueprint.post('/login')
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        raise InvalidRequestException("Missing username or password")

    user = User.query.filter_by(username=username).first()
    role = Role.query.filter_by(id=user.role_id).first()

    if not user:
        raise AuthenticationException('کاربر یافت نشد')

    if check_password_hash(user.password, password):
        # generates the JWT Token
        access_token = create_access_token(identity=user, additional_claims={'role': role.name})
        refresh_token = create_refresh_token(identity=user, additional_claims={'role': role.name})

        return {'user': user_schema.dump(user),
                'access_token': access_token,
                'refresh_token': refresh_token}
    raise AuthenticationException('نام کاربری یا پسورد نادرست است')


@auth_blueprint.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_use_token():
    access_token = create_access_token(identity=current_user)
    return {'access_token': access_token}, HTTP_200_OK


@auth_blueprint.post('/register')
def register():
    name = request.json.get('name')
    username = request.json.get('username')
    password = request.json.get('password')
    confirm = request.json.get('confirm')
    role_name = request.json.get('role')

    if password != confirm:
        raise InvalidRequestException('Password and Confirm should be equal')

    user = user_repo.find_by_username(username)
    role = Role.get_by_name(role_name)

    if not user:
        user = User(name=name, username=username, password=password)
        user.role_id = role.id

        # insert the user
        add_user(user)

        # generate the auth token
        access_token = create_access_token(identity=user, additional_claims={'role': role.name})
        refresh_token = create_refresh_token(identity=user, additional_claims={'role': role.name})

        return {'user': user_schema.dump(user),
                'access_token': access_token,
                'refresh_token': refresh_token}
    else:
        raise EntityAlreadyExistException('User already exists')
