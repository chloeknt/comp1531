from json import dumps
from flask import Flask, Blueprint, request
from src.users_v1 import users_all_v1, user_profile_v1, user_profile_setname_v1, \
                        user_profile_setemail_v1, user_profile_sethandle_v1, user_stats_v1, workspace_stats_v1
from src.users_v2 import download_photo, upload_photo_v1
from src.tokens import token_to_id

users_all = Blueprint('users_all',__name__)
user_profile = Blueprint('user_profile',__name__)
user_profile_setname = Blueprint('user_profile_setname',__name__)
user_profile_setemail = Blueprint('user_profile_setemail',__name__)
user_profile_sethandle = Blueprint('user_profile_sethandle',__name__)
user_profile_uploadphoto = Blueprint('user_profile_uploadphoto',__name__)
user_stats = Blueprint('user_stats', __name__)
workspace_stats = Blueprint('workspace_stats', __name__)

@users_all.route('/users/all/v1', methods=['GET'])
def get_all_users():
    # token
    token = request.args.get('token')
    token_to_id(token)
    return dumps(
        users_all_v1()
    )

@user_profile.route('/user/profile/v1', methods=['GET'])
def get_user_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    token_to_id(token)

    return dumps(
        user_profile_v1(int(u_id))
    )

@user_profile_setname.route('/user/profile/setname/v1', methods=['PUT'])
def set_user_name():
    data = request.get_json()

    token = data.get('token')
    name_first = data.get('name_first')
    name_last = data.get('name_last')
    auth_user_id = token_to_id(token)

    return dumps(
        user_profile_setname_v1(auth_user_id, name_first, name_last)
    )

@user_profile_setemail.route('/user/profile/setemail/v1', methods=['PUT'])
def set_user_email_v2():
    data = request.get_json()

    token = data.get('token')
    email = data.get('email')
    auth_user_id = token_to_id(token)

    return dumps(
        user_profile_setemail_v1(auth_user_id, email)
    )

@user_profile_sethandle.route('/user/profile/sethandle/v1', methods=['PUT'])
def set_user_handle_v2():
    data = request.get_json()

    token = data.get('token')
    handle_str = data.get('handle_str')
    auth_user_id = token_to_id(token)

    return dumps(
        user_profile_sethandle_v1(auth_user_id, handle_str)
    )

@user_profile_uploadphoto.route('/user/profile/uploadphoto/v1', methods=['POST'])
def set_user_photo_v1():
    data = request.get_json()

    token = data.get('token')
    auth_user_id = token_to_id(token)
    img_url = data.get('img_url')
    x_start = data.get('x_start')
    y_start = data.get('y_start')
    x_end = data.get('x_end')
    y_end = data.get('y_end')

    return dumps(
        upload_photo_v1(auth_user_id, img_url, x_start, y_start, x_end, y_end)
    )

@user_stats.route('/user/stats/v1', methods=['GET'])
def get_user_stats():
    token = request.args.get('token')
    auth_user_id = token_to_id(token)

    return dumps(
        user_stats_v1(int(auth_user_id))
    )

@workspace_stats.route('/users/stats/v1', methods=['GET'])
def get_workspace_stats():
    token = request.args.get('token')
    auth_user_id = token_to_id(token)

    return dumps(
        workspace_stats_v1(auth_user_id)
    )
