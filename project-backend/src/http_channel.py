from json import dumps
from flask import Flask, Blueprint, request
from src.helper_functions.helpers import validate_auth_user, validate_channel, validate_u_id
from src.tokens import token_to_id
from src.iter1.channel_v1 import channel_details_v1, channel_invite_v1, channel_join_v1, channel_messages_v1
from src.channel_add_remove_owner_v1 import addowner_v1, removeowner_v1
from src.channel_leave_v1 import leave_v1

channel_details = Blueprint('channel_details', __name__)
channel_invite = Blueprint('channel_invite', __name__)
channel_join = Blueprint('channel_join', __name__)
channel_leave = Blueprint('channel_leave',__name__)
channel_messages = Blueprint('channel_messages', __name__)
channel_addowner = Blueprint('channel_addowner', __name__)
channel_removeowner = Blueprint('channel_removeowner', __name__)



@channel_details.route('/channel/details/v2', methods=['GET'])
def get_channel_details_v2():
    # token
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    # get a user id using the token
    auth_user_id = token_to_id(token)

    # get channel details
    channel = channel_details_v1(int(auth_user_id), int(channel_id))

    return dumps({
        'name': channel['name'],
        'is_public': channel['is_public'],
        'owner_members': channel['owner_members'],
        'all_members': channel['all_members']
    })


@channel_invite.route('/channel/invite/v2', methods=['POST'])
def process_invite():
    data = request.get_json()
    token = data.get('token')
    channel_id = data.get('channel_id')
    u_id = data.get('u_id')

    auth_id = token_to_id(token)

    channel_invite_v1(int(auth_id), int(channel_id), int(u_id))

    return dumps({})


@channel_join.route('/channel/join/v2', methods=['POST'])
def process_join():
    data = request.get_json()

    token = data.get('token')
    channel_id = data.get('channel_id')

    auth_id = token_to_id(token)

    channel_join_v1(int(auth_id), int(channel_id))

    return {}

@channel_leave.route('/channel/leave/v1', methods=['POST'])
def process_leave():
    data = request.get_json()

    token = data.get('token')
    channel_id = data.get('channel_id')
    
    auth_id = token_to_id(token)

    leave_v1(int(auth_id), int(channel_id))

    return {}

@channel_addowner.route('/channel/addowner/v1', methods=['POST'])
def process_addowner_request():
    data = request.get_json()
    auth_token = data.get('token')
    channel_id = data.get('channel_id')
    u_id = data.get('u_id')

    auth_user_id = token_to_id(auth_token)

    validate_auth_user(auth_user_id)
    validate_channel(channel_id)
    validate_u_id(u_id)

    addowner_v1(auth_user_id, int(channel_id), int(u_id))

    return dumps({})


@channel_removeowner.route('/channel/removeowner/v1', methods=['POST'])
def process_removeowner_request():
    data = request.get_json()

    auth_token = data.get('token')
    channel_id = data.get('channel_id')
    u_id = data.get('u_id')

    auth_user_id = token_to_id(auth_token)

    validate_auth_user(auth_user_id)
    validate_channel(channel_id)
    validate_u_id(u_id)

    removeowner_v1(auth_user_id, int(channel_id), int(u_id))

    return dumps({})


@channel_messages.route('/channel/messages/v2', methods=['GET'])
def channel_messages_v2():
    data = request.args
    token = data['token']
    channel_id = data['channel_id']
    start = data['start']

    auth_user_id = token_to_id(token)

    return dumps(channel_messages_v1(auth_user_id, int(channel_id), int(start)))
