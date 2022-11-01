from json import dumps
from flask import Flask, Blueprint, request
from src.standups_v1 import standup_start_v1, standup_active_v1, standup_send_v1
from src.tokens import token_to_id

standup_start = Blueprint('standup_start',__name__)
standup_active = Blueprint('standup_active',__name__)
standup_send = Blueprint('standup_send',__name__)

@standup_start.route('/standup/start/v1', methods=['POST'])
def start_standup():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    length = data['length']

    auth_id = token_to_id(token)
    
    return dumps(
        standup_start_v1(token, auth_id, channel_id, length)
    )

@standup_active.route('/standup/active/v1', methods=['GET'])
def active_standup():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')

    return dumps(
        standup_active_v1(token, channel_id)
    )

@standup_send.route('/standup/send/v1', methods=['POST'])
def send_standup():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']

    return dumps(
        standup_send_v1(token, channel_id, message)
    )