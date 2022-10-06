from todos_app.repositories import db


class Project(db.Model):
    __tablename__ = "Project"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))

    tasks = db.relationship('Task', backref='Project')
    users = db.relationship('User', backref='Project')

    def __init__(self, name):
        self.name = name
