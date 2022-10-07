from todos_app.exceptions.entity_not_found_exception import EntityNotFoundException
from todos_app.repositories import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))

    users = db.relationship('User', backref='Role')

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_by_name(name):
        role = Role.query.filter_by(name=name).first()
        if not role:
            raise EntityNotFoundException('Invalid Role')
        return role
