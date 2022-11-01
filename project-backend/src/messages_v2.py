import re
from src.data_store import data_store
from src.dm import dm_list_v1, message_senddm_v1
from src.error import InputError, AccessError
from src.helper_functions.helpers import already_joined, validate_channel, already_joined_no_error, \
    active, user_in_dm, return_message_id, get_timestamp, validate_dm
from src.iter1.channels_v1 import channels_list_v1
from src.messages import locate_message, message_send_v1
from src.tokens import token_to_id

import threading


def message_react_v1(auth_user_id, to_react, react_id):
    '''
    Description:
        - Given a message within a channel or DM the authorised 
        user is part of, "react" to that particular message.

    Parameters:
        auth_user_id - ID of user reacting to a message
        to_unreact - message ID that indicates which message to react
        react_id - integer that refers to a particular reaction type

    Return:
        None

    Exceptions:
    InputError when any of:
        - message_id is not a valid message within a channel or DM that 
        the authorised user has joined
        - react_id is not a valid react ID
        - the message already has a react with ID react_id from the 
        authorised user

    Changes in data store:
        modifies messages 
    '''
    store = data_store.get()
    users = store['users']
    channels = store['channels']
    dms = store['dms']

    sender_id = None
    notification = None

    location = locate_message(to_react, store['channels'])
    chat_id = location[0]
    chat_type = 'channels'

    if chat_id is None:
        location = locate_message(to_react, store['dms'])
        chat_id = location[0]
        chat_type = 'dms'

    if chat_id is None:
        raise InputError(
            description='Message was not found, invalid message_id for user.')

    if not already_joined_no_error(auth_user_id, chat_id, store[chat_type]):
        raise InputError(
            description=f'The user is not a member of the {chat_type}')

    if react_id not in [1]:
        raise InputError(description='Invalid/Unimplemented react_id.')

    chats = store[chat_type]

    message_index = location[1]
    message_data = chats[chat_id]['messages'][message_index]

    if message_data['reacts'] == []:
        new_react = {
            'react_id': react_id,
            'u_ids': [auth_user_id],
            'is_this_user_reacted': auth_user_id == message_data['u_id']
        }

        message_data['reacts'].append(new_react)

    else:
        for react in message_data['reacts']:
            if react['react_id'] == react_id and auth_user_id in react['u_ids']:
                raise InputError(description='This user has already reacted')
            elif react['react_id'] == react_id and auth_user_id not in react['u_ids']:
                react['u_ids'].append(auth_user_id)

                if auth_user_id == message_data['u_id']:
                    react['is_this_user_reacted'] = True
                break

    sender_id = None
    notification = None

    if chat_type == 'dms':
        sender_id = dms[chat_id]['messages'][message_index]['u_id']
        notification = {
            'channel_id' : -1,
            'dm_id' : message_index,
            'notification_message' : f"{users[auth_user_id]['handle_str']} reacted to your message in {dms[chat_id]['name']}"
        }
    else:
        sender_id = channels[chat_id]['messages'][message_index]['u_id'] 
        notification = {
            'channel_id' : message_index,
            'dm_id' : -1,
            'notification_message' : f"{users[auth_user_id]['handle_str']} reacted to your message in {channels[chat_id]['name']}"
        }
    
    if users[sender_id].get('notifications', None) is None:
        users[sender_id]['notifications'] = []
    users[sender_id]['notifications'].insert(0, notification)
    
    chats[chat_id]['messages'][message_index] = message_data
    store['users'] = users
    store[chat_type] = chats
    data_store.set(store)
    return {}


def message_unreact_v1(auth_user_id, to_unreact, react_id):
    '''
    Description:
        - Given a message within a channel or DM the authorised 
        user is part of, remove a "react" to that particular message.

    Parameters:
        auth_user_id - ID of user unreacting to a message
        to_unreact - message ID that indicates which message to unreact
        react_id - integer that refers to a particular reaction type

    Return:
        None

    Exceptions:
    InputError when any of:
        - message_id is not a valid message within a channel or DM that 
        the authorised user has joined
        - react_id is not a valid react ID
        - the message does not contain a react with ID react_id from the 
        authorised user

    Changes in data store:
        modifies messages 
    '''
    store = data_store.get()

    location = locate_message(to_unreact, store['channels'])
    chat_id = location[0]
    chat_type = 'channels'

    if chat_id is None:
        location = locate_message(to_unreact, store['dms'])
        chat_id = location[0]
        chat_type = 'dms'

    if chat_id is None:
        raise InputError(
            description='Message was not found, invalid message_id for user.')

    if not already_joined_no_error(auth_user_id, chat_id, store[chat_type]):
        raise InputError(
            description=f'The user is not a member of the {chat_type}')

    if react_id not in [1]:
        raise InputError(description='Invalid/Unimplemented react_id.')

    chats = store[chat_type]
    message_index = location[1]
    message_data = chats[chat_id]['messages'][message_index]

    for react in message_data['reacts']:
        if react['react_id'] == react_id and auth_user_id in react['u_ids']:
            react['u_ids'].remove(auth_user_id)

            if auth_user_id == message_data['u_id']:
                react['is_this_user_reacted'] = False

            break
        elif react['react_id'] == react_id and auth_user_id not in react['u_ids']:
            raise InputError(
                description='The user has not made this reacted to the message')

    chats[chat_id]['messages'][message_index] = message_data
    store[chat_type] = chats
    data_store.set(store)
    return {}


def message_pin_v1(auth_user_id, to_pin):
    '''
    Description:
        - Given a message within a channel or DM, 
        mark as pinned.

    Parameters:
        auth_user_id - ID of user pinning the message
        to_pin - message ID that indicates which message to pin

    Return:
        None

    Exceptions:
    InputError when any of:
        - message_id is not a valid message within a channel or DM that 
        the authorised user has joined
        - the message is already pinned
    AccessError when:
        - message_id refers to a valid message in a joined channel/DM and
        the authorised user does not have owner permissions in the channel/DM
    
    Changes in data store:
        modifies channels/dms
    '''
    store = data_store.get()
    users = store['users']

    location = locate_message(to_pin, store['channels'])
    chat_id = location[0]
    chat_type = 'channels'

    if chat_id is None:
        location = locate_message(to_pin, store['dms'])
        chat_id = location[0]
        chat_type = 'dms'

    if chat_id is None:
        raise InputError(
            description='Message was not found, invalid message_id for user.')

    if not already_joined_no_error(auth_user_id, chat_id, store[chat_type]):
        raise InputError(
            description=f'The user is not a member of the {chat_type}')

    chats = store[chat_type]
    message_index = location[1]
    message_data = chats[chat_id]['messages'][message_index]

    if users[auth_user_id]['permission_id'] != 1 and not any(member['u_id'] == auth_user_id for member in chats[chat_id]['owner_members']):
        raise AccessError(
            description='The user does not have permission to pin messages.')

    if message_data['is_pinned']:
        raise InputError(description='The message has already been pinned')

    message_data['is_pinned'] = True

    chats[chat_id]['messages'][message_index] = message_data
    store[chat_type] = chats
    data_store.set(store)
    return {}


def message_unpin_v1(auth_user_id, to_unpin):
    '''
    Description:
        - Given a message within a channel or DM, 
        remove its mark as pinned.

    Parameters:
        auth_user_id - ID of user unpinning the message
        to_unpin - message ID that indicates which message to unpin

    Return:
        None

    Exceptions:
    InputError when any of:
        - message_id is not a valid message within a channel or DM that 
        the authorised user has joined
        - the message is not already pinned
    AccessError when:
        - message_id refers to a valid message in a joined channel/DM and
        the authorised user does not have owner permissions in the channel/DM
    
    Changes in data store:
        modifies channels/dms
    '''
    store = data_store.get()
    users = store['users']

    location = locate_message(to_unpin, store['channels'])
    chat_id = location[0]
    chat_type = 'channels'

    if chat_id is None:
        location = locate_message(to_unpin, store['dms'])
        chat_id = location[0]
        chat_type = 'dms'

    if chat_id is None:
        raise InputError(
            description='Message was not found, invalid message_id for user.')

    if not already_joined_no_error(auth_user_id, chat_id, store[chat_type]):
        raise InputError(
            description=f'The user is not a member of the {chat_type}')

    chats = store[chat_type]
    message_index = location[1]
    message_data = chats[chat_id]['messages'][message_index]

    if users[auth_user_id]['permission_id'] != 1 and not any(member['u_id'] == auth_user_id for member in chats[chat_id]['owner_members']):
        raise AccessError(
            description='The user does not have permission to unpin messages.')

    if not message_data['is_pinned']:
        raise InputError(description='The message is already not pinned')

    message_data['is_pinned'] = False
    chats[chat_id]['messages'][message_index] = message_data
    store[chat_type] = chats
    data_store.set(store)
    return {}


def message_sendlater_v1(token, channel_id, is_channel, message, time_sent):
    '''
    Description:
        - Send a message from the authorised user to the channel specified by 
        channel_id automatically at a specified time in the future.
    
    Parameters:
        token - token from the user sending the message
        channel_id - the channel where the message is being sent
        message - message intended to be sent as a string 
        time_sent - unix timestamp for message 

    Return:
        message_id - integer

    Exceptions:
    InputError when any of:
        - channel_id does not refer to a valid channel
        - length of message is over 1000 characters
        - time_sent is a time in the past
    AccessError when:
        - channel_id is valid and the authorised user is 
        not a member of the channel they are trying to post to
    
    Changes in data store
        modifies messages and channels
    '''
    read = data_store.get()
    channels = read['channels']
    dms = read['dms']

    auth_id = token_to_id(token)

    interval = time_sent - get_timestamp()

    if len(message) > 1000:
        raise InputError(description='Message is too long')
    if interval < 0:
        raise InputError(description='Invalid time')

    if is_channel:
        validate_channel(channel_id)
        already_joined(auth_id, channel_id, channels)
        funct = message_send_v1
    else:
        validate_dm(channel_id)
        if not user_in_dm(auth_id, channel_id, dms):
            raise AccessError(
                description='Requested user is not a member of the selected DM')
        funct = message_senddm_v1

    message_id = return_message_id()

    thread = threading.Timer(interval, funct, args=[
        auth_id, channel_id, message, message_id])
    thread.start()

    return {'message_id': message_id}

def share_message(auth_user_id, og_message_id, message, channel_id, dm_id):
    '''
    Description:
        - Sends message from channel/dm to another channel/dm where there  
        is an optional message in addition to the shared message, which will 
        be empty if no message is given. 

    Parameters:
        auth_user_id - ID of user sharing the message
        og_message_id - the ID of the original message
        message - the optional message in addition to the shared message, 
        and will be an empty string '' if no message is given.
        channel_id - the channel that the message is being shared to, and 
        is -1 if it is being sent to a DM
        dm_id - the DM that the message is being shared to, and is -1 if 
        it is being sent to a channel.

    Return:
        shared_message_id - ID of the new message

    Exceptions:
    InputError when any of:
        - both channel_id and dm_id are invalid
        - neither channel_id nor dm_id are -1      
        - og_message_id does not refer to a valid message within a channel/DM 
        that the authorised user has joined
        - length of message is more than 1000 characters
    AccessError when:
        - the pair of channel_id and dm_id are valid (i.e. one is -1, the other 
        is valid) and the authorised user has not joined the channel or DM they 
        are trying to share the message to

    Changes in data store:
        modifies messages and channel/dm data
    '''

    store = data_store.get()

    if dm_id == -1 and channel_id == -1:
        raise InputError(description='Error: Both channel and DM cannot be -1')

    if dm_id != -1 and channel_id != -1:
        raise InputError(description='Error: Cannot be sent to both channel and DM')
    
    # handle accesserror case
    if channel_id == -1:
        validate_dm(dm_id)
        if not user_in_dm(auth_user_id, dm_id, store['dms']):
            raise AccessError(description='User is not a member of the DM')
        destination_id = dm_id
        chat_type = 'dms'
    else:
        validate_channel(channel_id)
        already_joined(auth_user_id, channel_id, store['channels'])
        destination_id = channel_id
        chat_type = 'channels'

    location = locate_message(og_message_id, store['channels'])
    chat_id = location[0]

    if chat_id is None:
        location = locate_message(og_message_id, store['dms'])
        chat_id = location[0]

    if chat_id is None:
        raise InputError(description='Message not found')

    if not already_joined_no_error(auth_user_id, chat_id, store[chat_type]):
        raise InputError(description=f'The user is not a member of the {chat_type}')

    chats = store[chat_type]
    message_index = location[1]
    shared_message = chats[chat_id]['messages'][message_index]['message']

    formatted_message = f'{message}\n\n"""\n{shared_message}"""'

    if chat_type == 'channels':
        shared_message_id = message_send_v1(auth_user_id, destination_id, formatted_message)
    else:
        shared_message_id = message_senddm_v1(auth_user_id, destination_id, formatted_message)['message_id']
        store = data_store.get()

    return {
        'shared_message_id': shared_message_id
    }
