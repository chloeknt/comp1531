'''
channels.py - COMP1531 Team T09 Dodo
    Description:
        Implements functionality to create and read channels in UNSW Streams
'''

from src.data_store import data_store
from src.error import InputError, AccessError
import src.helper_functions.helpers as helper_funcs

def channels_list_v1(auth_user_id):
    '''
    Description:
        Given a user_id of an authorised user,
        returns a list of their joined channels.

    Parameters:
        auth_user_id - ID of user

    Return:
        {
            'channels': [{'channel_id', 'name'}, ...]
        } 
        
        Dictionary with a list of channel objects

    Changes in data_store:
        None, only reads

    AccessError when:
        auth_user_id is invalid
    '''

    read = data_store.get()
    channels = read['channels']

    helper_funcs.validate_auth_user(auth_user_id)

    user_channels_list = []

    for channel in helper_funcs.active(channels):
        # if channel contains auth_user_id, add it to the list
        if helper_funcs.already_joined_no_error(auth_user_id, channel['channel_id'], channels):
            user_channels_list.append(helper_funcs.get_channel_details(channel))

    return {'channels': user_channels_list}

def channels_listall_v1(auth_user_id):
    '''
    Description:
        Given a user_id of an authorised user,
        returns a list of all channels in UNSW Streams.

    Parameters:
        auth_user_id - ID of user

    Return:
        {
            'channels': [{'channel_id', 'name'}, ...]
        } 
        
        Dictionary with a list of channel objects

    Changes in data_store:
        None, only reads

    AccessError when:
        auth_user_id is invalid
    '''

    read = data_store.get()
    channels = read['channels']

    helper_funcs.validate_auth_user(auth_user_id)

    all_channels_list = []

    for channel in helper_funcs.active(channels):
        all_channels_list.append(helper_funcs.get_channel_details(channel))

    return {'channels': all_channels_list}

def channels_create_v1(auth_user_id, name, is_public):
    '''
    Description:
        Given an auth_user_id, name and channel privacy status,
        creates a new channel in UNSW Streams.

    Parameters:
        auth_user_id - ID of user
        name - name of new channel
        is_public - true or false value denoting privacy status

    Return:
        {'channel_id': int} - Dictionary encapsulating channel_id int

    Changes in data_store:
        increments session_channels
        appends to channels list in datastore

    InputError when:
        length of name is less than 1 or more than 20 characters

    AccessError when:
        auth_user_id is invalid
    '''

    store = data_store.get()
    users = store['users']
    channels = store['channels']
    session_channels = store['session_channels']

    # validate arguments
    helper_funcs.validate_auth_user(auth_user_id)

    if isinstance(name, str):
        if len(name) < 1 or len(name) > 20:
            raise InputError( description='The channel name must be between 1 and 20 characters long')

    # create new channel
    new_channel_id = session_channels
    session_channels += 1

    new_channel = {
        'name': name.strip(),
        'is_public': is_public,
        'owner_members': [helper_funcs.get_user_details(users[auth_user_id])],
        'all_members': [helper_funcs.get_user_details(users[auth_user_id])],
        'channel_id': new_channel_id,
        'messages': []
    }

    channels.append(new_channel)

    store['channels'] = channels
    store['session_channels'] = session_channels
    data_store.set(store)

    return {'channel_id': new_channel_id}
