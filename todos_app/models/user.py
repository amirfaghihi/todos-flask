from werkzeug.security import generate_password_hash, check_password_hash

from todos_app.models.usertask import user_task
from flask_rbac import UserMixin

from todos_app.repositories import db


class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String)

    role = db.relationship('Role', uselist=False, backref='role')
    tasks = db.relationship('Task', secondary=user_task, backref='Users')

    project_id = db.Column(db.Integer, db.ForeignKey('Project.id'))

    def __init__(self, username, password, name):
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name

    def add_role(self, role):
        self.role = role

    def get_roles(self):
        return self.role

    def add_task(self, task_obj):
        self.tasks.append(task_obj)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)
