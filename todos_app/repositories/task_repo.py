from todos_app.exceptions.entity_not_found_exception import EntityNotFoundException
from todos_app.models import Task


def find_by_id(id: int) -> Task:
    entity = Task.query.filter_by(id=id).first()
    if not entity:
        raise EntityNotFoundException
    return entity
