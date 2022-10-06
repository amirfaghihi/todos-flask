from datetime import datetime

from todos_app.repositories import db


class Task(db.Model):
    __tablename__ = 'Task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(80))
    description = db.Column(db.String(120))
    story_points = db.Column(db.Integer)

    project_id = db.Column(db.Integer, db.ForeignKey('Project.id'))

    deadline = db.Column(db.DateTime, default=datetime.now())
