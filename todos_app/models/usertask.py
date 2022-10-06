from todos_app.repositories import db

user_task = db.Table('user_task',
                     db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
                     db.Column('task_id', db.Integer, db.ForeignKey('Task.id'), primary_key=True))
