'''
helpers.py - COMP1531 Team T09 Dodo
    Description:
        Helper functions for UNSW Streams functions
'''

from datetime import timezone, datetime

from src.data_store import data_store
from src.error import InputError, AccessError
import src.iter1.channels_v1 as channels_iter1
from src.dm import dm_list_v1
from datetime import datetime, timezone

''' contains commonly used helper functions '''

# def modify_reacted_messages(auth_user_id, messages):


# def modify_reacted_by(auth_user_id, chats):

def active(list):
    ''' Returns a list of active elements given a list. I.E. returns only elements that are not None'''
    return [elem for elem in list if elem is not None]


def get_user_details(user):
    ''' returns a dictionary without the user's password or permissions '''
    return {
        'u_id': user['u_id'],
        'email': user['email'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'handle_str': user['handle_str'],
        'profile_img_url': user['profile_img_url']
    }


def validate_channel(channel_id):
    ''' throws an InputError if a given channel_id is invalid '''
    read = data_store.get()
    channels = read['channels']
    session_channels = read['session_channels']

    if not (isinstance(channel_id, int)):
        raise InputError('Not a valid channel id, must be an integer')

    if channel_id < 0 or channel_id >= session_channels:
        raise InputError('This channel has not been created')

    if channels[channel_id] is None:
        raise InputError('This channel has been deleted')


def validate_dm(dm_id):
    ''' throws an InputError if a given dm_id is invalid '''
    read = data_store.get()
    dms = read['dms']
    session_dms = read['session_dms']

    if not (isinstance(dm_id, int)):
        raise InputError('Not a valid dm id, must be an integer')

    if dm_id < 0 or dm_id >= session_dms:
        raise InputError('This dm has not been created')

    if dms[dm_id] is None:
        raise InputError('This dm has been deleted')


def validate_auth_user(auth_user_id):
    ''' throws an AccessError if an auth_user_id is invalid (as per spec 6.3)'''
    read = data_store.get()
    session_users = read['session_users']
    users = read['users']

    if not(isinstance(auth_user_id, int)):
        raise AccessError('Not a valid user id, must be an integer')

    if auth_user_id < 0 or auth_user_id >= session_users:
        raise AccessError('This user has not been registered')
    elif users[auth_user_id]['name_first'] == 'Removed' and users[auth_user_id]['name_last'] == 'user':
        raise AccessError('This user has been deleted')

    return {}


def validate_u_id(u_id):
    ''' throws an InputError if an u_id is invalid (as per spec 6.3)'''
    read = data_store.get()
    session_users = read['session_users']
    users = read['users']

    if u_id < 0 or u_id >= session_users:
        raise InputError('This user has not been registered')
    elif users[u_id]['name_first'] == 'Removed' and users[u_id]['name_last'] == 'user':
        raise InputError('This user has been deleted')

    return {}


def id_in_channel(u_id, channel_id):
    ''' throws InputError if a u_id is invalid (as per spec 6.3)'''
    read = data_store.get()
    session_users = read['session_users']
    users = read['users']
    channels = read['channels']

    if user_in_channel(u_id, channel_id, channels):
        raise InputError('Requested user already a member of channel')

    if u_id < 0 or u_id >= session_users:
        raise InputError('This user has not been registered')
    if users[u_id]['name_first'] == 'Removed' and users[u_id]['name_last'] == 'user':
        raise InputError('This user has been deleted')

    return {}


def user_in_channel(auth_user_id, channel_id, channels):
    ''' checks if a user is in the channel '''
    for user in channels[channel_id]['all_members']:
        if auth_user_id == user['u_id']:
            return True
    return False


def user_in_dm(auth_user_id, dm_id, dms):
    ''' checks if a user is in the dm '''
    for user in dms[dm_id]['all_members']:
        if auth_user_id == user['u_id']:
            return True

    return False


def already_joined_no_error(u_id, channel_id, channels):
    ''' checks whether a user is a member of given channel'''
    if not user_in_channel(u_id, channel_id, channels):
        return False

    return True


def already_joined(u_id, channel_id, channels):
    ''' checks whether a user is a member of given channel'''

    if not user_in_channel(u_id, channel_id, channels):
        raise AccessError('The user is not a member of the channel')

    return True


def get_channel_details(channels_list):
    ''' returns a subset of form { channel_id, name } from the given channel '''
    return {
        'channel_id': channels_list['channel_id'],
        'name': channels_list['name']
    }


def msg_search_and_replace(auth_user_id, message_id, new_message):
    store = data_store.get()
    channels = store['channels']
    dms = store['dms']

    for channel in active(channels):
        for message in channel['messages']:
            if message_id == message['message_id']:
                message['message'] = 'Removed user'
        store['channels'] = channels
        data_store.set(store)

    for dm in active(dms):
        for message in dm['messages']:
            if message_id == message['message_id']:
                message['message'] = 'Removed user'
        store['dms'] = dms
        data_store.set(store)


# returns a list of all message ids sent by a particular u_id
def get_messages(u_id):
    read = data_store.get()
    channels = read['channels']
    dms = read['dms']

    message_ids = []

    for channel in active(channels):
        for message in channel['messages']:
            if u_id == message['u_id']:
                message_ids.append(message['message_id'])

    for dm in active(dms):
        for message in dm['messages']:
            if u_id == message['u_id']:
                message_ids.append(message['message_id'])

    return message_ids


def return_global_owners(users):
    global_owners = 0
    for user in users:
        if user['permission_id'] == 1:
            global_owners += 1

    return global_owners

# def get_timestamp():
#     dt = datetime.now()
#     timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
#     return int(timestamp)

def get_num_users_in_channel_or_dm(auth_user_id):
    store = data_store.get()
    users_list = store['users']

    total_in_channel_or_dm = 0

    # users = users_list[auth_user_id]
    for user in users_list:
        curr_user_id = user['u_id']
        in_channel = False
        in_dm = False

        # for channel in channels:
        #     if curr_user in channel['all_members']:
        #         in_channel = True
        #         break;
        
        # number of channels user is in
        num_channels_joined = len(channels_iter1.channels_list_v1(curr_user_id)['channels'])
        if num_channels_joined > 0:
            in_channel = True

        # number of dms user is in
        num_dms_joined = len(dm_list_v1(curr_user_id))
        if num_dms_joined > 0:
            in_dm = True
        
        if in_channel or in_dm:
            total_in_channel_or_dm += 1
        

    return total_in_channel_or_dm

def get_timestamp():

    return int(datetime.now().replace(tzinfo=timezone.utc).timestamp())


def return_message_id():
    store = data_store.get()
    session_messages = store['session_messages']

    message_id = session_messages
    session_messages += 1

    store['session_messages'] = session_messages
    data_store.set(store)
    return message_id
