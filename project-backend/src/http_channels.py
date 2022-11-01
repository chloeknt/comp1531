from json import dumps
from flask import Flask, Blueprint, request
from src.iter1.channels_v1 import channels_create_v1, channels_list_v1, channels_listall_v1
from src.tokens import token_to_id

channels_create = Blueprint('channels_create',__name__)
channels_list = Blueprint('channels_list', __name__)
channels_listall = Blueprint('channels_listall', __name__)

@channels_create.route('/channels/create/v2', methods=['POST'])
def process_channels_create():
    data = request.get_json()
    token = data['token']
    
    auth_id = token_to_id(token)

    channel_name = data['name']
    is_public = bool(data['is_public'])

    return dumps(
        channels_create_v1(auth_id, channel_name, is_public)
    )

@channels_list.route('/channels/list/v2', methods=['GET'])
def list_channels():
    ''' Channels list route '''
    token = request.args.get('token')
    auth_id = token_to_id(token)

    return dumps(
        channels_list_v1(auth_id)
    )

@channels_listall.route('/channels/listall/v2', methods=['GET'])
def list_all_channels():
    ''' Channels listall route '''
    token = request.args.get('token')
    auth_id = token_to_id(token)

    return dumps(
        channels_listall_v1(auth_id)
    )