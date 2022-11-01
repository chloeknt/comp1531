from src.error import AccessError, InputError

from src.data_store import *
from src.helper_functions.helpers import user_in_channel, validate_auth_user, validate_u_id, validate_channel, id_in_channel, get_user_details

def addowner_v1(auth_id, channel_id, u_id):
    '''
    Arguments:
    -    Token (string)
    -    Channel_id (int)
    -    U_id (int)
    Exceptions:
    -    InputError occurs 
    -    channel_id does not refer to a valid channel
    -    u_id does not refer to a valid user
    -    u_id refers to a user who is not a member of the channel
    -    u_id refers to a user who is already an owner of the channel
    AccessError occurs 
    -    channel_id is valid and the authorised user does not have owner permissions in the channel
        Return Value:
    -    Returns {}
    '''

    store = data_store.get()
    users = store['users']
    channels = store['channels']

    if not any(user['u_id'] == auth_id for user in channels[channel_id]['owner_members']) and not users[auth_id]['permission_id'] == 1:
        raise AccessError(description ='The auth_user is not an owner')

    if not user_in_channel(u_id, channel_id, channels):
        raise InputError(description='The user must be a member to be promoted to channel owner')

    if any(user['u_id'] == u_id for user in channels[channel_id]['owner_members']):
        raise InputError(description='The user to promote is already an owner of the requested channel')

    channels[channel_id]['owner_members'].append(get_user_details(users[u_id]))

    store['channels'] = channels
    data_store.set(store)

def removeowner_v1(auth_id, channel_id, u_id):
    store = data_store.get()
    users = store['users']
    channels = store['channels']

    if not any(user['u_id'] == auth_id for user in channels[channel_id]['owner_members']) and not users[auth_id]['permission_id'] == 1:
        raise AccessError(description ='The auth_user is not an owner')

    if not any(user['u_id'] == u_id for user in channels[channel_id]['owner_members']):
        raise InputError(description ='The u_id provided is not an owner of the requested channel')

    if len(channels[channel_id]['owner_members']) <= 1:
        raise InputError(description ='You cannot remove the only owner of a channel')

    channels[channel_id]['owner_members'].remove(get_user_details(users[u_id]))

    store['channels'] = channels
    data_store.set(store)
