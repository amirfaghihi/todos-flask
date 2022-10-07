from datetime import datetime, timedelta

from todos_app.repositories import db


class Task(db.Model):
    __tablename__ = 'Task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(80))
    description = db.Column(db.String(120))
    story_points = db.Column(db.Integer)

    project_id = db.Column(db.Integer, db.ForeignKey('Project.id'))

    deadline = db.Column(db.DateTime, default=datetime.now() + timedelta(days=7))

    def __init__(self, title, description, story_points, deadline):
        self.title = title
        self.description = description
        self.story_points = story_points
        self.deadline = deadline
