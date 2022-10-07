from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from todos_app.blueprints import rbac
from todos_app.exceptions.invalid_request_exception import InvalidRequestException
from todos_app.repositories import project_repo, user_repo, task_repo
from todos_app.responses.base_response import BaseResponse
from todos_app.schemas.task_schema import tasks_schema
from todos_app.utils.http_status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT

task_blueprint = Blueprint(name='task_blueprint', import_name=__name__, url_prefix='/v1/task')


@task_blueprint.get('/all')
@rbac.allow(['developer'], methods=['GET'])
def get_tasks():
    if not current_user.project_id:
        raise InvalidRequestException('User does not have a project')

    project = project_repo.find_by_id(current_user.project_id)

    tasks = tasks_schema.dump(project.tasks)
    meta = {
        'page': tasks.page,
        'pages': tasks.pages,
        'total_count': tasks.total,
        'prev_page': tasks.prev_num,
        'next_page': tasks.next_num
    }
    response_data = {'tasks': tasks, 'meta': meta}
    response = BaseResponse(http_status='OK', http_status_code=HTTP_200_OK, data=response_data)

    return response.to_dict(), response.http_status_code


@task_blueprint.get('/self')
@jwt_required()
@rbac.allow(['developer'], methods=['GET'])
def get_tasks_for_user():
    tasks = tasks_schema.dump(current_user.tasks)
    meta = {
        'page': tasks.page,
        'pages': tasks.pages,
        'total_count': tasks.total,
        'prev_page': tasks.prev_num,
        'next_page': tasks.next_num
    }
    response_data = {'tasks': tasks, 'meta': meta}
    response = BaseResponse(http_status='OK', http_status_code=HTTP_200_OK, data=response_data)

    return response.to_dict(), response.http_status_code


@task_blueprint.post('/assign')
@jwt_required()
@rbac.allow(['project_manager'], methods=['POST'])
def assign_task():
    assignee_id = int(request.args.get('assignee'))
    task_id = int(request.args.get('task_id'))

    task_obj = task_repo.find_by_id(task_id)
    user_repo.add_task_to_user(assignee_id, task_obj)

    response = BaseResponse(http_status='UPDATED', http_status_code=HTTP_204_NO_CONTENT, data={})

    return response.to_dict(), response.http_status_code


