from email.message import Message
import re
from src.data_store import data_store
from src.error import InputError, AccessError
from src.helper_functions.helpers import already_joined, validate_channel, already_joined_no_error, \
    active, get_timestamp, return_message_id
from datetime import datetime, timezone, date


def locate_message(message_id, chats):
    for chat in active(chats):
        for message_index in range(len(chat['messages'])):
            if chat['messages'][message_index]['message_id'] == message_id:
                try:
                    return (chat['channel_id'], message_index)
                except KeyError:
                    return (chat['dm_id'], message_index)

    return (None, None)


def message_send_v1(auth_user_id, channel_id, message, message_id=-1):
    '''
    Arguments:
    -    Token (string)
    -    Channel_id (int)
    -    Message (string)
    Exceptions:
    -    InputError occurs 
    -    channel_id does not refer to a valid channel
    -    length of message is less than 1 or over 1000 characters
    -    AccessError occurs 
    -    channel_id is valid and the authorised user is not a member of the channel

    Return Value:
        Returns {‘message_id’ : (int)}
    '''

    # Grab channels from data_store
    store = data_store.get()
    channels = store['channels']
    users = store['users']

    # InputError: channel_id is invalid
    validate_channel(channel_id)

    # AccessError: channel_id is valid and authorised user is not a channel member
    already_joined(auth_user_id, channel_id, channels)

    # InputError: length of message < 1 or > 1000 characters
    if len(message) < 1 or len(message) > 1000:
        raise InputError(description='The message is not of a valid length.')

    if message_id == -1:
        message_id = return_message_id()
    "{user_handle} tagged you in {channel/dm_id}: (first 20 characters of message including the tag)"
    # User handle from auth user id
    # Append notification to tagged user's notifications list 
    sent_handle = None
    for user in users:
        if user['u_id'] == auth_user_id:
            sent_handle = user['handle_str']
    channel_name = None
    for channel in channels:
        if channel['channel_id'] == channel_id:
            channel_name = channel['name']

    for user in users:
        handle = '@' + user['handle_str']
        if re.search(rf'{handle}', message):
            if re.search(rf'{handle}\w', message):
                continue

            if user.get('notifications') is None:
                user['notifications'] = []
            new_notif = {
                'channel_id' : channel_id,
                'dm_id' : -1,
                'notification_message' : f'{sent_handle} tagged you in {channel_name}: {message[:20]}'
            }
            user['notifications'].insert(0, new_notif)

    new_message = {
        'message_id': message_id,
        'u_id': auth_user_id,
        'message': message,
        'time_created': get_timestamp(),
        'reacts': [
            {
                'react_id': 1,
                'u_ids': [],
                'is_this_user_reacted': False
            }
        ],
        'is_pinned': False
    }

    channels[channel_id]['messages'].insert(0, new_message)

    store['users'] = users
    store['channels'] = channels
    data_store.set(store)

    return message_id

def message_edit_v1(auth_user_id, to_edit, new_message):
    '''
    Arguments:
    -    Token (string)
    -    Message_id (int)
    -    Message (string)
    Exceptions:
    -    InputError occurs 
    -    length of message is over 1000 characters
    -    message_id does not refer to a valid message within a channel/DM that the authorised user has joined
    -    AccessError occurs when message_id refers to a valid message in a joined channel/DM and none of the following are true:
    -    the message was sent by the authorised user making this request
    -    the authorised user has owner permissions in the channel/DM
    Return Value:
        Returns {}
    '''

    store = data_store.get()
    users = store['users']
    dms = store['dms']
    channels = store['channels']

    location = locate_message(to_edit, store['channels'])
    chat_id = location[0]
    chat_type = 'channels'

    if chat_id is None:
        location = locate_message(to_edit, store['dms'])
        chat_id = location[0]
        chat_type = 'dms'

    if chat_id is None:
        raise InputError(
            description='Message was not found, invalid message_id.')

    chats = store[chat_type]
    message_index = location[1]
    message_data = chats[chat_id]['messages'][message_index]

    # delete message if empty
    if len(new_message) <= 0:
        message_remove_v1(auth_user_id, to_edit)
        return {}

    if len(new_message) < 1 or len(new_message) > 1000:
        raise InputError(description='The message is not of a valid length.')

    if not already_joined_no_error(auth_user_id, chat_id, chats):
        raise InputError(
            description='Accessing invalid channel user has not yet joined.')

    if users[auth_user_id]['permission_id'] != 1 and message_data['u_id'] != auth_user_id:
        raise AccessError(
            description='You cannot edit a message you did not send.')

    message_data['message'] = new_message

    chats[chat_id]['messages'][message_index] = message_data
    
    sent_handle = None
    for user in users:
        if user['u_id'] == chats[chat_id]['messages'][message_index]['u_id']:
            sent_handle = user['handle_str']
    name = None
    if chat_type == 'dms':
        name = dms[chat_id]['name']
        new_notif = {
            'dm_id' : chat_id,
            'channel_id' : -1,
            'notification_message' : ''
        }
    else:
        name = channels[chat_id]['name']
        new_notif = {
            'dm_id' : -1,
            'channel_id' : chat_id,
            'notification_message' : ''
        }
    for user in users:
        handle = '@' + user['handle_str']
        if handle in new_message:
            if user.get('notifications', None) is None:
                user['notifications'] = []
            new_notif['notification_message'] = f'{sent_handle} tagged you in {name}: {new_message[:20]}'
            user['notifications'].insert(0, new_notif)
    store[chat_type] = chats
    store['users'] = users
    data_store.set(store)
    return {}


def message_remove_v1(auth_user_id, to_delete):
    """ 
    Arguments:
    -    Token (string)
    -    Message_id (int)
    Exceptions:
    -    InputError occurs 
    -    message_id does not refer to a valid message within a channel/DM that the authorised user has joined
    -    AccessError occurs when message_id refers to a valid message in a joined channel/DM and none of the following are true:
    -    the message was sent by the authorised user making this request
    -    the authorised user has owner permissions in the channel/DM
    Return Value:
        Returns {} 
    """

    store = data_store.get()
    users = store['users']

    location = locate_message(to_delete, store['channels'])
    chat_id = location[0]
    chat_type = 'channels'

    if chat_id is None:
        location = locate_message(to_delete, store['dms'])
        chat_id = location[0]
        chat_type = 'dms'

    if chat_id is None:
        raise InputError(
            description='Message was not found, invalid message_id.')

    chats = store[chat_type]
    message_index = location[1]
    message_data = chats[chat_id]['messages'][message_index]

    if not already_joined_no_error(auth_user_id, chat_id, chats):
        raise InputError(
            description='Accessing invalid channel user has not yet joined.')

    if users[auth_user_id]['permission_id'] != 1 and message_data['u_id'] != auth_user_id:
        raise AccessError(
            description='You cannot edit a message you did not send.')

    chats[chat_id]['messages'].pop(message_index)
    store[chat_type] = chats
    data_store.set(store)
    return {}
