from json import dumps
from flask import Flask, Blueprint, request
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, dm_leave_v1, dm_messages_v1, message_senddm_v1
from src.tokens import token_to_id

dm_create = Blueprint('dm_create', __name__)
dm_list = Blueprint('dm_list', __name__)
dm_remove = Blueprint('dm_remove', __name__)
dm_details = Blueprint('dm_details', __name__)
dm_leave = Blueprint('dm_leave', __name__)
dm_messages = Blueprint('dm_messages', __name__)
message_senddm = Blueprint('message_senddm', __name__)


@dm_create.route('/dm/create/v1', methods=['POST'])
def dms_create_v1():
    ''' Dms create route '''
    data = request.get_json()

    # look at the data and grab info from it
    token = data.get('token')
    u_ids = data.get('u_ids')
    auth_user_id = token_to_id(token)
    # u_ids into ints
    new_u_ids = []
    for u_id in u_ids:
        new_u_id = int(u_id)
        new_u_ids.append(new_u_id)

    dm_result = dm_create_v1(auth_user_id, new_u_ids)
    dm_id = dm_result.get('dm_id')

    return dumps({
        'dm_id': dm_id
    })


@dm_list.route('/dm/list/v1', methods=['GET'])
def get_dm_list_v1():
    ''' Dms list route '''
    token = request.args.get('token')
    auth_user_id = token_to_id(token)
    dms_list = dm_list_v1(auth_user_id)

    return dumps({
        'dms': dms_list
    })


@dm_remove.route('/dm/remove/v1', methods=['DELETE'])
def delete_dm_remove_v1():
    data = request.get_json()

    token = data.get('token')
    dm_id = data.get('dm_id')

    auth_user_id = token_to_id(token)

    return dm_remove_v1(auth_user_id, int(dm_id))


@dm_details.route('/dm/details/v1', methods=['GET'])
def get_dm_details_v1():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')

    auth_user_id = token_to_id(token)

    dm_details = dm_details_v1(auth_user_id, int(dm_id))

    return dumps({
        'name': dm_details['name'],
        'members': dm_details['members']
    })


@dm_leave.route('/dm/leave/v1', methods=['POST'])
def post_dm_leave_v1():
    data = request.get_json()

    token = data.get('token')
    dm_id = data.get('dm_id')
    auth_user_id = token_to_id(token)

    return dm_leave_v1(auth_user_id, int(dm_id))


@dm_messages.route('/dm/messages/v1', methods=['GET'])
def get_dm_messages_v1():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start')

    auth_user_id = token_to_id(token)

    channel = dm_messages_v1(auth_user_id, int(dm_id), int(start))

    return dumps({
        'messages': channel['messages'],
        'start': channel['start'],
        'end': channel['end']
    })


@message_senddm.route('/message/senddm/v1', methods=['POST'])
def post_message_senddm_v1():
    data = request.get_json()

    token = data.get('token')
    dm_id = data.get('dm_id')
    message = data.get('message')
    auth_user_id = token_to_id(token)

    message_id = message_senddm_v1(auth_user_id, int(dm_id), message)

    return dumps({
        'message_id': message_id['message_id']
    })
