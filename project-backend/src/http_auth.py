from json import dumps
from flask import Flask, Blueprint, request
from src.iter1.auth_v1 import auth_login_v1, auth_register_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.tokens import encode_token, token_to_id
from src.data_store import data_store
from src.helper_functions.auth_helpers import validate_password
import hashlib 

auth_login = Blueprint('auth_login', __name__)
auth_register = Blueprint('auth_register', __name__)
auth_logout = Blueprint('auth_logout', __name__)
auth_passwordreset_request = Blueprint('auth_passwordreset_request', __name__)
auth_passwordreset_reset = Blueprint('auth_passwordreset_reset', __name__)

@auth_login.route('/auth/login/v2', methods=['POST'])
def post_auth_login_v2():
    # grab data from json
    data = request.get_json()

    # look at the data and grab info from it
    email = data.get('email')
    password = data.get('password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # grab the user_id from login function
    user = auth_login_v1(email, hashed_password)
    auth_user_id = user.get('auth_user_id')

    # token
    token = encode_token(auth_user_id)

    store = data_store.get()
    users = store['users']

    if users[auth_user_id].get('active_tokens', None) is None:
        users[auth_user_id]['active_tokens'] = []
        
    users[auth_user_id]['active_tokens'].append(token)

    store['users'] = users
    data_store.set(store)

    return dumps({
        'token' : token,
        'auth_user_id' : auth_user_id
    })

@auth_register.route('/auth/register/v2', methods=['POST'])
def post_auth_register_v2():
    data = request.json

    # look at data and grab info from it
    email = data.get('email')
    password = data.get('password')
    name_first = data.get('name_first')
    name_last = data.get('name_last')
    validate_password(password)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # get data and then register the user
    user_details = auth_register_v1(email, hashed_password, name_first, name_last)
    auth_user_id = user_details.get('auth_user_id')

    # token
    token = encode_token(auth_user_id)

    store = data_store.get()
    users = store['users']

    if users[auth_user_id].get('active_tokens', None) is None:
        users[auth_user_id]['active_tokens'] = []

    users[auth_user_id]['active_tokens'].append(token)

    store['users'] = users
    data_store.set(store)

    return dumps({
        'token' : token,
        'auth_user_id' : auth_user_id
    })

@auth_logout.route('/auth/logout/v1', methods=['POST'])
def post_auth_logout_v1():
    '''
    Arguments:
      - Token (string)

    Exceptions:
      - N/a

    Return Value:
      - Returns {}
    '''

    data = request.get_json()

    # token
    token = data.get('token')

    auth_user_id = token_to_id(token)

    store = data_store.get()
    users = store['users']
    users[auth_user_id]['active_tokens'].remove(token)

    store['users'] = users
    data_store.set(store)

    return dumps({})

@auth_passwordreset_request.route('/auth/passwordreset/request/v1', methods=['POST'])
def post_passwordreset_request():
    data = request.get_json()

    email = data.get('email')

    auth_passwordreset_request_v1(email)

    return dumps({})

@auth_passwordreset_reset.route('/auth/passwordreset/reset/v1', methods=['POST'])
def post_passwordreset_reset_v1():
    data = request.get_json()

    reset_code = data.get('reset_code')
    new_password = data.get('new_password')

    auth_passwordreset_reset_v1(reset_code, new_password)

    return dumps({})
