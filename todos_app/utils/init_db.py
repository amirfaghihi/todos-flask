from datetime import datetime, timedelta

from todos_app.models import Task, Project
from todos_app.models.role import Role
from todos_app.repositories import db


def init_db():
    try:
        role1 = Role("developer")
        role2 = Role("project_manager")
        db.session.add(role1)
        db.session.add(role2)
        task1 = Task(title="t1", description="task1", story_points=5, deadline=datetime.now() + timedelta(days=3))
        db.session.add(task1)
        task2 = Task(title="t2", description="task2", story_points=1, deadline=datetime.now() + timedelta(days=9))
        db.session.add(task2)
        p1 = Project("p1")
        db.session.add(p1)
        p2 = Project("p2")
        db.session.add(p2)
        p1.tasks.append(task1)
        p2.tasks.append(task2)
        db.session.commit()
    except Exception:
        db.session.rollback()
        print("error!!")
