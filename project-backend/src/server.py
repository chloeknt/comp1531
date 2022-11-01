import sys
import signal
from json import dumps
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.config import port, IMGURL_DIR

from src.http_channel import channel_invite, channel_details, channel_join, channel_messages, channel_leave, channel_addowner, channel_removeowner
from src.http_channels import channels_create, channels_list, channels_listall
from src.http_auth import auth_login, auth_register, auth_logout, auth_passwordreset_request, auth_passwordreset_reset
from src.http_dms import dm_create, dm_list, dm_remove, dm_details, dm_leave, dm_messages, message_senddm
from src.http_users import users_all, user_profile, user_profile_setname, \
    user_profile_setemail, user_profile_sethandle, user_stats, workspace_stats, user_profile_uploadphoto
from src.http_messages import message_send, message_sendlater, message_edit, message_delete, message_react, message_unreact, message_pin, message_unpin,\
    message_sendlaterdm, message_share
from src.http_standups import standup_start, standup_active, standup_send
from src.http_admin import admin_user_permission_change, admin_user_remove
from src.http_notifications_get import notifications_get
from src.http_search import search
from src.http_clear import clear

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        'code': err.code,
        'name': 'System Error',
        'message': err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)

#### REGISTERING SUBFILES HERE ####
APP.register_blueprint(auth_login)
APP.register_blueprint(auth_register)
APP.register_blueprint(auth_logout)
APP.register_blueprint(auth_passwordreset_request)
APP.register_blueprint(auth_passwordreset_reset)

APP.register_blueprint(channels_create)
APP.register_blueprint(channels_list)
APP.register_blueprint(channels_listall)

APP.register_blueprint(channel_invite)
APP.register_blueprint(channel_details)
APP.register_blueprint(channel_join)
APP.register_blueprint(channel_leave)
APP.register_blueprint(channel_messages)
APP.register_blueprint(channel_addowner)
APP.register_blueprint(channel_removeowner)

APP.register_blueprint(dm_create)
APP.register_blueprint(dm_list)
APP.register_blueprint(dm_remove)
APP.register_blueprint(dm_details)
APP.register_blueprint(dm_leave)
APP.register_blueprint(dm_messages)
APP.register_blueprint(message_senddm)

APP.register_blueprint(users_all)
APP.register_blueprint(user_profile)
APP.register_blueprint(user_profile_setname)
APP.register_blueprint(user_profile_setemail)
APP.register_blueprint(user_profile_sethandle)
APP.register_blueprint(user_profile_uploadphoto)
APP.register_blueprint(user_stats)
APP.register_blueprint(workspace_stats)

APP.register_blueprint(message_send)
APP.register_blueprint(message_edit)
APP.register_blueprint(message_delete)
APP.register_blueprint(message_react)
APP.register_blueprint(message_unreact)
APP.register_blueprint(message_pin)
APP.register_blueprint(message_unpin)
APP.register_blueprint(message_sendlater)
APP.register_blueprint(message_sendlaterdm)
APP.register_blueprint(message_share)

APP.register_blueprint(standup_start)
APP.register_blueprint(standup_active)
APP.register_blueprint(standup_send)

APP.register_blueprint(search)

APP.register_blueprint(admin_user_permission_change)
APP.register_blueprint(admin_user_remove)

APP.register_blueprint(clear)

APP.register_blueprint(notifications_get)


CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS
@APP.route('/imgurl/<path:filename>', methods=['GET'])
def serve_profile_photo(filename):
    return send_from_directory(IMGURL_DIR, filename)
# NO NEED TO MODIFY BELOW THIS POINT


if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=port, debug=False)  # Do not edit this port
