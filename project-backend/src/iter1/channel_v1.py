'''
channel.py - COMP1531 Team T09 Dodo
    Description:
        Implements functionality to allow user interaction with channels in UNSW Streams
'''

from src.data_store import data_store
from src.error import InputError, AccessError
from src.helper_functions.helpers import user_in_channel, get_user_details, already_joined,\
                        id_in_channel, validate_auth_user, validate_channel

def channel_invite_v1(auth_user_id, channel_id, u_id):
    '''
    Description:
        Given an authorised user, channel_id and an invited user,
        will add the invitee to the channel if not already a member

    Parameters:
        auth_user_id - ID of user inviting another to the channel
        channel_id - ID of the channel
        u_id - ID of invitee

    Return:
        {} - Empty dictionary

    Changes in data_store:
        appends to the 'all_members' list of the given channel 

    InputError when any of:
        channel_id does not refer to a valid channel
        u_id does not refer to a valid user
        u_id refers to a member who is already in the channel

    AccessError when:
        channel_id is valid and the authorised user is not a member of the channel
        auth_user_id is not valid
    '''

    store = data_store.get()
    users = store['users']
    channels = store['channels']

    validate_auth_user(auth_user_id)
    validate_channel(channel_id)

    if not user_in_channel(auth_user_id, channel_id, channels):
        raise AccessError( description='User not a member of requested channel')
    
    id_in_channel(u_id, channel_id)

    invitee = users[u_id]

    # add the user to the channel
    channels[channel_id]['all_members'].append(get_user_details(invitee))

    notification = {
        'channel_id' : channel_id,
        'dm_id' : -1,
        'notification_message' :  f"{users[auth_user_id]['handle_str']} added you to {channels[channel_id]['name']}"
    }

    if users[u_id].get('notifications') is None:
        users[u_id]['notifications'] = []
    users[u_id]['notifications'].insert(0, notification)
    
    # save change to store
    store['channels'] = channels
    store['users'] = users
    data_store.set(store)
    return {}

def channel_details_v1(auth_user_id, channel_id):
    '''
    Description:
        Given an authorised user and channel_id returns basic channel details

    Parameters:
        auth_user_id - ID of user who is a member of the channel
        channel_id - ID of the channel

    Return:
        {
            'name' : name of channel,
            'is_public' : channel privacy status,
            'owner_members' : list of owners,
            'all_members' : list of all members
        }

    Changes in data_store:
        None, only reads

    InputError when any of:
        channel_id does not refer to a valid channel

    AccessError when:
        channel_id is valid and the authorised user is not a member of the channel
        auth_user_id is not valid
    '''

    read = data_store.get()
    channels = read['channels']

    validate_auth_user(auth_user_id)
    validate_channel(channel_id)

    # check if the user is in the channel
    already_joined(auth_user_id, channel_id, channels)

    name = channels[channel_id]['name']
    is_public = channels[channel_id]['is_public']

    return {
            'name' : name,
            'is_public' : is_public,
            'owner_members' : channels[channel_id]['owner_members'],
            'all_members' : channels[channel_id]['all_members']
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    '''
    Description:
        Given an authorised user, channel_id and start index,
        returns paginated chunk of messages

    Parameters:
        auth_user_id - ID of user who is a member of the channel
        channel_id - ID of the channel
        start - index from which to fetch at most 50 more messages

    Return:
        {
            'messages' : list of dictionaries containing messages,
            'start' : start index,
            'end' : start + 50 or -1 if all messages have been fetched
        }

    Changes in data_store:
        None, only reads

    InputError when any of:
        channel_id does not refer to a valid channel
        start is greater than the total number of messages in the channel

    AccessError when:
        channel_id is valid and the authorised user is not a member of the channel
        auth_user_id is not valid
    '''

    read = data_store.get()
    channels = read['channels']
    
    validate_auth_user(auth_user_id)
    validate_channel(channel_id)

    if not already_joined(auth_user_id, channel_id, channels):
        raise AccessError( description='Not a member of channel requested')

    if start < 0:
        raise InputError( description='Invalid message start index')

    index = 0
    loaded_chunk = []
    end = -1

    # fetch 50 messages between indexes and append them to the loaded_chunk list
    for message in channels[channel_id]['messages']:
        if index == start + 50:
            end = start + 50
            break
        elif index >= start:
            loaded_chunk.append(message)
        index += 1

    if index < start:
        raise InputError( description='Message index requested greater than messages in channel')

    return {
            'messages' : loaded_chunk,
            'start' : start,
            'end' : end
    }


def channel_join_v1(auth_user_id, channel_id):
    '''
    Description:
        Given a channel_id of a channel that the authorised user can join,
        adds them to that channel.

    Parameters:
        auth_user_id - ID of user who wishes to join
        channel_id - ID of the channel

    Return:
        {} - Empty dictionary

    Changes in data_store:
        appends to the 'all_members' list of the given channel
        appends to the 'owner_members' list of the given channel

    InputError when any of:
        channel_id does not refer to a valid channel
        the authorised user is already a member of the channel

    AccessError when:
        auth_user_id is not valid
        channel_id refers to a channel that is private
            AND the authorised user is not already a channel member
            AND is not a global owner
    '''

    store = data_store.get()
    channels = store['channels']
    users = store['users']

    validate_auth_user(auth_user_id)
    validate_channel(channel_id)

    if user_in_channel(auth_user_id, channel_id, channels):
        raise InputError( description='The user is already a member of the given channel')

    if not channels[channel_id]['is_public']:
        if users[auth_user_id]['permission_id'] != 1:    
            raise AccessError( description='This user does not have permission to join the private channel')

    # add user to channel members list
    channels[channel_id]['all_members'].append(get_user_details(users[auth_user_id]))

    # save changes
    store['channels'] = channels
    data_store.set(store)

    return {}
