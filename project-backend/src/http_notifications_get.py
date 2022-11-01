from json import dumps
from flask import Flask, Blueprint, request
from src.notifications_get import notifications_get_v1
from src.tokens import token_to_id

notifications_get = Blueprint('notifications_get',__name__)

@notifications_get.route('/notifications/get/v1', methods=['GET'])
def get_notifications():
    # token
    token = request.args.get('token')
    return dumps(
        notifications_get_v1(token_to_id(token))
    )