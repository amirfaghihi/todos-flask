from flask import Blueprint, request
from flask_jwt_extended import current_user
from todos_app.exceptions.invalid_request_exception import InvalidRequestException
from todos_app.repositories import project_repo, user_repo, task_repo
from todos_app.responses.base_response import BaseResponse
from todos_app.schemas.task_schema import tasks_schema
from todos_app.utils.http_status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT
from todos_app.utils.role_required import role_required

task_blueprint = Blueprint(name='task_blueprint', import_name=__name__, url_prefix='/v1/task')


@task_blueprint.get('/all')
@role_required(['developer'])
def get_tasks():
    if not current_user.project_id:
        raise InvalidRequestException('User does not have a project')

    project = project_repo.find_by_id(current_user.project_id)

    tasks = tasks_schema.dump(project.tasks)

    response_data = {'tasks': tasks}
    response = BaseResponse(http_status='OK', http_status_code=HTTP_200_OK, data=response_data)

    return response.to_dict(), response.http_status_code


@task_blueprint.get('/self')
@role_required(['developer'])
def get_tasks_for_user():
    tasks = tasks_schema.dump(current_user.tasks)
    response_data = {'tasks': tasks}
    response = BaseResponse(http_status='OK', http_status_code=HTTP_200_OK, data=response_data)

    return response.to_dict(), response.http_status_code


@task_blueprint.post('/assign')
@role_required(['project_manager'])
def assign_task():
    assignee_id = int(request.json.get('assignee'))
    task_id = int(request.json.get('task_id'))

    task_obj = task_repo.find_by_id(task_id)
    user_obj = user_repo.find_by_id(assignee_id)

    if task_obj.project_id != user_obj.project_id:
        raise InvalidRequestException('Task is from another project')

    user_repo.add_task_to_user(assignee_id, task_obj)

    response = BaseResponse(http_status='UPDATED', http_status_code=HTTP_204_NO_CONTENT, data={})

    return response.to_dict(), response.http_status_code


