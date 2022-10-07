import os
import yaml
from flask import Flask
from flask_cors import CORS
from todos_app.schemas import ma
from todos_app.repositories import db
from flask_jwt_extended import JWTManager

from todos_app.blueprints.authentication import auth_blueprint
from todos_app.blueprints.project import project_blueprint
from todos_app.blueprints.task import task_blueprint
from todos_app.exceptions.api_exception import ApiException
from todos_app.models import User
from todos_app.responses.base_response import BaseResponse


def load_config():
    config_path = os.environ.get('config_path', '../application.yml')
    with open(config_path, 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    return config


def create_app(config):
    app_config = config['app']
    db_config = config['db']

    app = Flask(__name__, instance_relative_config=True)
    app.config['ENV'] = app_config['env']
    app.config['DEBUG'] = app_config['debug']
    app.config['SECRET_KEY'] = app_config['secret_key']
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['RBAC_USE_WHITE'] = False
    if app_config['env'] == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = '{}://{}:{}@{}:{}/{}'.format(db_config['driver'],
                                                                             db_config['username'],
                                                                             db_config['password'],
                                                                             db_config['host'],
                                                                             db_config['port'],
                                                                             db_config['name'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app_config['sqlalchemy_track_modifications']
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt = JWTManager(app)
    db.app = app
    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(task_blueprint)
    app.register_blueprint(project_blueprint)

    @app.errorhandler(ApiException)
    def handle_api_exception(error: ApiException):
        return BaseResponse(http_status=error.http_status,
                            http_status_code=error.http_status_code,
                            data={}, error=error.to_dict()).to_dict(), error.http_status_code

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(id=identity).one_or_none()

    return app


config = load_config()
app = create_app(config)
db.create_all()
