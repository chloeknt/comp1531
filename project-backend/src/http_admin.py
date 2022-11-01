from json import dumps
from flask import Flask, Blueprint, request
from src.tokens import token_to_id
from src.admin_v1 import permission_change_v1, user_remove_v1

admin_user_permission_change = Blueprint(
    'admin_user_permission_change', __name__)
admin_user_remove = Blueprint(
    'admin_user_remove', __name__)


@admin_user_permission_change.route('/admin/userpermission/change/v1', methods=['POST'])
def process_join():
    data = request.get_json()

    token = data.get('token')
    u_id = int(data.get('u_id'))
    permission_id = data.get('permission_id')

    auth_id = token_to_id(token)

    permission_change_v1(auth_id, u_id, permission_id)

    return {}


@admin_user_remove.route('/admin/user/remove/v1', methods=['DELETE'])
def remove_user():
    data = request.get_json()

    token = data.get('token')
    u_id = int(data.get('u_id'))

    auth_id = token_to_id(token)

    user_remove_v1(auth_id, u_id)

    return {}
