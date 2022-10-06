from todos_app.exceptions.entity_not_found_exception import EntityNotFoundException
from todos_app.models import Project


def find_all(page: int, per_page: int):
    return Project.query.order_by(Project.id.asc()).paginate(page=page, per_page=per_page)


def find_by_id(id: int) -> Project:
    entity = Project.query.filter_by(id=id).first()
    if not entity:
        raise EntityNotFoundException
    return entity
