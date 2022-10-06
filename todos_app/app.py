from flask import Flask
from flask_cors import CORS
from flask_rbac import RBAC

from todos_app.blueprints.authentication import auth_blueprint
from todos_app.blueprints.user import user_blueprint
from todos_app.exceptions.api_exception import ApiException
from todos_app.models import User, Coupon
from todos_app.repository import db
from todos_app.response.base_response import BaseResponse

from todos_app.models.role import Role
from todos_app.schemas import ma
from flask_jwt_extended import JWTManager
import yaml

rbac = RBAC()


def load_config():
    with open('./application.yml', 'r') as config_file:
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
    rbac.init_app(app)
    rbac.set_role_model(Role)
    rbac.set_user_model(User)
    db.app = app
    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)

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


def init_db():
    from datetime import datetime, timedelta

    app = create_app()
    with app.app_context():
        db.create_all()

    # define some users
    user1 = User(username="a.faghihi", name="Amirhossein Faghihi",
                 password="password", credit=100)
    user2 = User(username="user2", name="user2", password="user2pass", credit=500)
    user3 = User(username="user3", name="user3", password="user3pass", credit=50)
    user4 = User(username="user4", name="user4", password="user4pass", credit=1500)
    user5 = User(username="user5", name="user5", password="user5pass", credit=20)
    user6 = User(username="user6", name="user6", password="user6pass", credit=175)

    # define some coupons

    coupon1 = Coupon(name="one", value=50, hidden_code="ABC", number_left=5,
                     expiration_date=datetime.now() + timedelta(days=10))
    coupon2 = Coupon(name="two", value=450, hidden_code="BCD", number_left=3,
                     expiration_date=datetime.now() + timedelta(days=1))
    coupon3 = Coupon(name="three", value=350, hidden_code="CDE", number_left=12,
                     expiration_date=datetime.now() + timedelta(hours=5))
    coupon4 = Coupon(name="four", value=250, hidden_code="DEF", number_left=1,
                     expiration_date=datetime.now() + timedelta(hours=1))
    coupon5 = Coupon(name="five", value=150, hidden_code="EFG", number_left=4,
                     expiration_date=datetime.now() + timedelta(minutes=10))

    db.session.add_all([user1, user2, user3, user4, user5, user6])
    db.session.add_all([coupon1, coupon2, coupon3, coupon4, coupon5])
    db.session.commit()


if __name__ == "__main__":
    # init_db()

    config = load_config()
    app = create_app(config)
    with app.app_context():
        db.create_all()

    app.run(host=config['app']['host'], port=config['app']['port'])
