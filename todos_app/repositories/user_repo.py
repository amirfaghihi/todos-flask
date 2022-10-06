from todos_app.exceptions.database_exception import DatabaseException
from todos_app.exceptions.entity_not_found_exception import EntityNotFoundException
from todos_app.models import User
from todos_app.repositories import db


def find_by_id(id: int) -> User:
    entity = User.query.filter_by(id=id).first()
    if not entity:
        raise EntityNotFoundException
    return entity


def add_task_to_user(user_id: int, task_obj):
    try:
        user = find_by_id(user_id)
        user.tasks.append(task_obj)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise DatabaseException('An Error occurred in operation')


def find_by_username(username: str):
    return User.query.filter_by(username=username).one_or_none()
