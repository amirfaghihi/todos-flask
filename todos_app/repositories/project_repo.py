from todos_app.exceptions.database_exception import DatabaseException
from todos_app.exceptions.entity_not_found_exception import EntityNotFoundException
from todos_app.models import Project, User
from todos_app.repositories import db


def find_all(page: int, per_page: int):
    return Project.query.order_by(Project.id.asc()).paginate(page=page, per_page=per_page)


def find_by_id(id: int) -> Project:
    entity = Project.query.filter_by(id=id).first()
    if not entity:
        raise EntityNotFoundException
    return entity


def add_user_to_project(username, project_id):
    try:
        project = Project.query.filter_by(id=project_id).first()
        user = User.query.filter_by(username=username).first()
        project.users.append(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise DatabaseException('Error occurred')

