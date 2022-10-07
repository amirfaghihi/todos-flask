from flask import Blueprint, request

from todos_app.repositories.project_repo import add_user_to_project

from todos_app.responses.base_response import BaseResponse
from todos_app.utils.http_status_codes import HTTP_204_NO_CONTENT
from todos_app.utils.role_required import role_required

project_blueprint = Blueprint(name='project_blueprint', import_name=__name__, url_prefix='/v1/project')


@project_blueprint.post('/assign')
@role_required(['project_manager'])
def assign_user_to_project():
    username = request.json.get('username')
    project_id = request.json.get('project_id')

    add_user_to_project(username, project_id)

    response = BaseResponse(http_status='UPDATED', http_status_code=HTTP_204_NO_CONTENT, data={})

    return response.to_dict(), response.http_status_code
