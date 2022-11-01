from json import dumps
from flask import Flask, Blueprint, request
from src.messages import message_send_v1, message_edit_v1, message_remove_v1
from src.messages_v2 import message_react_v1, message_unreact_v1, message_pin_v1, message_unpin_v1, message_sendlater_v1, share_message
from src.tokens import token_to_id

message_send = Blueprint('message_send', __name__)
message_sendlater = Blueprint('message_sendlater', __name__)
message_sendlaterdm = Blueprint('message_sendlaterdm', __name__)
message_edit = Blueprint('message_edit', __name__)
message_delete = Blueprint('message_delete', __name__)
message_react = Blueprint('message_react', __name__)
message_unreact = Blueprint('message_unreact', __name__)
message_pin = Blueprint('message_pin', __name__)
message_unpin = Blueprint('message_unpin', __name__)
message_share = Blueprint('message_share', __name__)


@message_send.route('/message/send/v1', methods=['POST'])
def send_message():
    data = request.get_json()
    token = data['token']
    message = data['message']
    channel_id = data['channel_id']

    message_id = message_send_v1(token_to_id(token), int(channel_id), message)

    return dumps({'message_id': message_id})


@message_edit.route('/message/edit/v1', methods=['PUT'])
def edit_message():
    data = request.get_json()
    token = data.get('token')
    message = data.get('message')
    message_id = data.get('message_id')

    return dumps(message_edit_v1(token_to_id(token), int(message_id), message))


@message_delete.route('/message/remove/v1', methods=['DELETE'])
def delete_message():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']

    return dumps(message_remove_v1(token_to_id(token), int(message_id)))


@message_react.route('/message/react/v1', methods=['POST'])
def react_to_message():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    react_id = data['react_id']

    return dumps(message_react_v1(token_to_id(token), int(message_id), int(react_id)))


@message_unreact.route('/message/unreact/v1', methods=['POST'])
def unreact_to_message():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    react_id = data['react_id']

    return dumps(message_unreact_v1(token_to_id(token), int(message_id), int(react_id)))


@message_pin.route('/message/pin/v1', methods=['POST'])
def pin_message():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']

    return dumps(message_pin_v1(token_to_id(token), int(message_id)))


@message_unpin.route('/message/unpin/v1', methods=['POST'])
def unpin_message():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']

    return dumps(message_unpin_v1(token_to_id(token), int(message_id)))


@message_sendlater.route('/message/sendlater/v1', methods=['POST'])
def send_later():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    message = data['message']
    time_sent = data['time_sent']

    return dumps(message_sendlater_v1(token, channel_id, True, message, int(time_sent)))


@message_sendlaterdm.route('/message/sendlaterdm/v1', methods=['POST'])
def send_later_dm():
    data = request.get_json()
    token = data['token']
    dm_id = int(data['dm_id'])
    message = data['message']
    time_sent = data['time_sent']

    return dumps(message_sendlater_v1(token, dm_id, False, message, int(time_sent)))

@message_share.route('/message/share/v1', methods=['POST'])
def share():
    data = request.get_json()
    token = data['token']
    auth_id = token_to_id(token)
    og_id = data['og_message_id']
    if data.get('message') is not None:
        message = data['message']
    else:
        message = ''
    channel_id = int(data['channel_id'])
    dm_id = int(data['dm_id'])

    return dumps(share_message(auth_id, og_id, message, channel_id, dm_id))