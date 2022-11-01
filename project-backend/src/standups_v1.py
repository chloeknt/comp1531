'''
standups_v1.py - COMP1531 Team T09 Dodo
    Description:
        Implements functionality regarding standup information for UNSW Streams
'''

from src.data_store import data_store
from src.error import InputError, AccessError
from src.helper_functions.auth_helpers import validate_email, validate_name
from src.helper_functions.helpers import get_timestamp, validate_channel, user_in_channel
from src.tokens import token_to_id

from src.messages import message_send_v1

from datetime import date, datetime, timedelta, timezone
import time
import threading
import requests
from src.config import url


def standup_start_v1(token, auth_id, channel_id, length):
    '''
    Description:
        - For a given channel, start the standup period whereby for the 
        next "length" seconds if someone calls "standup/send" with a message, 
        it is buffered during the X second window then at the end of the X 
        second window a message will be added to the message queue in the channel 
        from the user who started the standup. "length" is an integer that denotes 
        the number of seconds that the standup occurs for.

    Parameters:
        token - token of the user starting the standup
        auth_id - user that is starting the standup
        channel_id - channel that the standup is being started in
        length - seconds that the standup occurs for 

    Return:
        time_finish - unix timestamp

    Exceptions:
    InputError when any of:
        - channel_id does not refer to a valid channel
        - length is a negative integer
        - an active standup is currently running in the channel
    AccessError when:
        - channel_id is valid and the authorised user is not a member of the channel

    Changes to data store:
        modifies channels
    '''
    store = data_store.get()
    channels = store['channels']
    session_channels = store['session_channels']

    try:
        channel_id = int(channel_id)
    except ValueError:
        validate_channel(channel_id)

    validate_channel(channel_id)
    channel = channels[channel_id]

    # check length is not negative
    if length < 0:
        raise InputError(description="Length cannot be negative!")
    else:
        length = int(length)

    # check if a standup is already active in the channel
    ret = standup_active_v1(token, channel_id)
    if ret['is_active'] == True:
        raise InputError(description="This channel already has an active standup!")

    # check user is a member of the channel
    if channel_id < 0 or channel_id >= session_channels:
        raise InputError(description="This channel does not exist.")
    if not user_in_channel(auth_id, channel_id, channels):
        raise AccessError('User is not a member of the channel.')

    dt = datetime.now()+timedelta(seconds=length)
    finish_timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())

    # add information to datastore:
    channel['standup_info'] = {}
    channel['standup_info']['user'] = auth_id
    channel['standup_info']['is_active'] = True
    channel['standup_info']['time_finish'] = finish_timestamp
    channel['standup_info']['queue'] = []

    data_store.set(store)

    standup_thread = threading.Timer(
        length, send_standup_messages, args=[channel_id, token])
    standup_thread.start()

    return {
        'time_finish': finish_timestamp
    }


def send_standup_messages(channel_id, token):
    '''
    Description:

    Parameters:

    Return:

    Exceptions:

    Changes to data store:
    '''
    channel_id = int(channel_id)

    store = data_store.get()
    channels = store['channels']
    session_channels = store['session_channels']
    standup_data = channels[channel_id]['standup_info']
    auth_id = token_to_id(token)

    # check user is a member of the channel
    if channel_id < 0 or channel_id >= session_channels:
        raise InputError(description="This channel does not exist.")
    if not user_in_channel(auth_id, channel_id, channels):
        raise AccessError('User is not a member of the channel.')

    message_string = ''
    for queued_message in standup_data['queue']:
        message_string += queued_message
        message_string += '\n'

    '''
        two options:
            one - create formal post request (need token)
            two - add to data_store and assume pagination will
                  take care of the rest
    '''

    # one
    requests.post(f'{url}message/send/v1', json={
        'token': token,
        'message': message_string[:-1],
        'channel_id': channel_id
    })

    # two
    #message_send_v1(standup_data['user'], channel_id, message_string)

    # clear the standup_info object once message has been sent
    store['channels'][channel_id]['standup_info'] = {}
    data_store.set(store)

    return {}


def standup_active_v1(token, channel_id):
    '''
    Description:
        - For a given channel, return whether a 
        standup is active in it, and what time the standup 
        finishes. If no standup is active, then time_finish 
        returns None.

    Parameters:
        auth_user_id - user requesting to check if standup is active
        channel_id - channel where the check is being performed

    Return:
        is_active - bool indicating standup active status
        time_finish - unix timestamp

    Exceptions:
    InputError when:
        - channel_id does not refer to a valid channel
    AccessError when:
        - channel_id is valid and the authorised user is not a member of the channel

    Changes to data store:
        modifies channels
    '''
    store = data_store.get()
    channels = store['channels']
    auth_user_id = token_to_id(token)

    try:
        channel_id = int(channel_id)
    except ValueError:
        validate_channel(channel_id)

    channel_id = int(channel_id)
    validate_channel(channel_id)
    channel = channels[channel_id]

    # validate user is member of channel
    if not user_in_channel(auth_user_id, channel_id, channels):
        raise AccessError(description="User is not a member of this channel")

    dt = datetime.now()
    current_timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())

    is_active = False
    time_finish = None

    if channel.get('standup_info') != None:
        if channel['standup_info'].get('is_active') == True:
            is_active = True
            time_finish = channel['standup_info']['time_finish']

    # check if standup has finished yet
    if is_active == True and time_finish != None:
        if current_timestamp > time_finish:
            is_active = False
            time_finish = None
            channel['standup_info']['is_active'] = is_active
            channel['standup_info']['time_finish'] = time_finish
    
    data_store.set(store)

    return {'is_active': is_active, 'time_finish': time_finish}


def standup_send_v1(token, channel_id, message):
    '''
    Description:
        - Sending a message to get buffered in the standup 
        queue, assuming a standup is currently active.

    Parameters:
        token - token of the user sending the message
        channel_id - channel where the message is being sent
        message - string containing message to be sent

    Return:
        None

    Exceptions:
    InputError when any of:
        - channel_id does not refer to a valid channel
        - length of message is over 1000 characters
        - an active standup is not currently running in the channel
    AccessError when:
        - channel_id is valid and the authorised user is not a member of the channel

    Changes to data store:
        modifies messages and channels
    '''
    store = data_store.get()
    channels = store['channels']
    users = store['users']

    auth_id = token_to_id(token)
    channel_id = int(channel_id)
    validate_channel(channel_id)

    if not user_in_channel(auth_id, channel_id, channels):
        raise AccessError('User not in channel')
    if len(message) > 1000:
        raise InputError('Message is too long')

    if not standup_active_v1(token, channel_id)['is_active']:
        raise InputError('No standup is currently active')

    standup_data = channels[channel_id]['standup_info']
    message_handle = users[auth_id]['handle_str']
    queued_message = message_handle + ': ' + message

    standup_data['queue'].append(queued_message)
    channels[channel_id]['standup_info'] = standup_data
    store['channels'] = channels
    data_store.set(store)

    return {}
