import jwt
from requests.sessions import session
from src.data_store import data_store
from src.error import AccessError
from src.helper_functions.helpers import validate_auth_user

SECRET = 'possessive_authority'

def encode_token(auth_user_id):
    '''
    Encodes the received auth_user_id into a JWT token with the provided secret.
    '''
    store = data_store.get()
    session_id = store['total_session_ids']
    new_token = jwt.encode({'auth_user_id': auth_user_id, 'session_id': session_id}, SECRET, algorithm='HS256')

    store['total_session_ids'] += 1
    data_store.set(store)

    return new_token

def decode_token(encoded_jwt):
    '''
    Decodes the received JWT token into the user's auth_user_id.
    '''
    try:
        output = jwt.decode(encoded_jwt.encode('utf-8'), SECRET, algorithms=['HS256'])
        return output
    except (jwt.InvalidTokenError, jwt.DecodeError) as token_errors:
        raise AccessError(description='Token cannot be decoded.') from token_errors


def verify_token(token):
    '''
    Decodes token and checks whether it is active for the user.
    '''
    values = decode_token(token)
    user_id = values['auth_user_id']
    
    store = data_store.get()
    users = store['users']

    validate_auth_user(user_id)

    if token in users[user_id]['active_tokens']:
        return True
    
    return False

def token_to_id(token):
    ''' 
    Verifies and decodes token to return auth_user_id
    '''
    if not verify_token(token):
        raise AccessError(description='An invalid token was used')

    auth_user_id = decode_token(token)['auth_user_id']

    return auth_user_id