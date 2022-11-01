import re

from requests.sessions import session
from src.data_store import data_store
from src.error import InputError, AccessError
# import src.helper_functions.helpers as helper_funcs
from datetime import datetime, timezone, date
import src.helper_functions.helpers as helper_funcs

def dm_create_v1(auth_user_id, u_ids):
    '''
    Parameters: {Auth_user_id (integer)}
    
    InputError when:
        - any u_id in u_ids does not refer to a valid user

    AccessError when:
        N/A
    Return Value: {dm_id (integer)}
    '''
    
    store = data_store.get()
    users = store['users']
    session_users = store['session_users']
    dms = store['dms']
    session_dms = store['session_dms']

    # InputError when:
    # any u_id in u_ids does not refer to a valid user
    for u_id in u_ids:
        if u_id < 0 or u_id >= session_users:
            raise InputError(description='This user has not been registered')
        if users[u_id]['name_first'] == 'Removed' and users[u_id]['name_last'] == 'user':
            raise InputError(description='This user has been deleted')

    # Get the new dm_id of the dm
    new_dm_id = session_dms
    session_dms += 1

    # Naming the dm
    dm_name_list = []
    for user in users:
        if user['u_id'] == auth_user_id:
            dm_name_list.append(user['handle_str'])
        else:
            for u_id in u_ids:
                if user['u_id'] == u_id:
                    dm_name_list.append(user['handle_str'])
    dm_name_list.sort()
    new_dm_name = ', '.join(dm_name_list)

    # Get owner of the DM and put it into data_store
    # assuming auth_user_id is decoded auth_u_id...

    new_dm_owner_members = [helper_funcs.get_user_details(users[auth_user_id])]

    new_dm_members = []
    for member in new_dm_owner_members:
        new_dm_members.append(member)

    for u_id in u_ids:
        new_dm_members.append(helper_funcs.get_user_details(users[u_id]))

    new_dm = {
        'dm_id': new_dm_id,
        'name': new_dm_name,
        'owner_members': new_dm_owner_members,
        'all_members': new_dm_members,
        'messages': []
    }

    dms.append(new_dm)

    store['dms'] = dms
    store['session_dms'] = session_dms
    store['users'] = users
    data_store.set(store)

    for u_id in u_ids:
        notification = {
            'channel_id' : -1,
            'dm_id' : new_dm_id,
            'notification_message' :  f"{users[auth_user_id]['handle_str']} added you to {dms[new_dm_id]['name']}"
        }

        if users[u_id].get('notifications') is None:
            users[u_id]['notifications'] = []
        users[u_id]['notifications'].insert(0, notification)

    return {'dm_id': new_dm_id}


def dm_list_v1(auth_user_id):
    '''
    Parameters: {Auth_user_id (integer)}
    Remove an existing DM, so all members are no longer in the DM. 
    This can only be done by the original creator of the DM.
    
    InputError when:
        N/A

    AccessError when:
        N/A
    Return Value: {dms (list of dm dictionaries)}
    '''

    store = data_store.get()
    user_dms = store['dms']

    user_dms_list = []

    for dm in helper_funcs.active(user_dms):
        if any(member['u_id'] == auth_user_id for member in dm['all_members']):
            new_dm = {
                'dm_id': dm['dm_id'],
                'name': dm['name']
            }
            user_dms_list.append(new_dm)
    
    # helper_funcs.modify_reacted_dms(auth_user_id, user_dms_list)

    return user_dms_list


def dm_remove_v1(auth_user_id, dm_id):
    '''
    Remove an existing DM, so all members are no longer in the DM.
    This can only be done by the original creator of the DM.

    InputError when:
        dm_id does not refer to a valid DM

    AccessError when:
        dm_id is valid and the authorised user is not the original DM creator
    '''
    store = data_store.get()
    dms = store['dms']
    session_dms = store['session_dms']

    # InputError when:
    # dm_id does not refer to a valid DM
    if dm_id < 0 or dm_id >= session_dms:
        raise InputError(description='This dm does not exist')
    if dms[dm_id] is None:
        raise InputError(description='This dm has been deleted')

    # AccessError when:
        # dm_id is valid and the authorised user is not the original DM creator
    if not any(member['u_id'] == auth_user_id for member in dms[dm_id]['owner_members']):
        raise AccessError(description='This user cannot delete the dm.')

    # Soft delete the dm
    dms[dm_id] = None
    store['dms'] = dms
    data_store.set(store)

    return {}


def dm_details_v1(auth_user_id, dm_id):
    '''
    Parameters:
        {auth_user_id (integer), dm_id (integer)}
    InputError when:
        dm_id does not refer to a valid DM
    AccessError when:
        dm_id is valid and the authorised user is not a member of the DM
    Return Value: {name (integer), members (member dictionary)}
    '''
    
    store = data_store.get()
    dms = store['dms']
    session_dms = store['session_dms']

    # InputError: dm_id does not refer to a valid DM
    if dm_id >= session_dms or dm_id < 0:
        raise InputError(description='This dm has not been created')

    if dms[dm_id] is None:
        raise InputError(description='This dm has been deleted')

    # AccessError when:
    # -> dm_id is valid and the authorised user is not a member of the DM
    if not any(member['u_id'] == auth_user_id for member in dms[dm_id]['all_members']):
        raise AccessError(description='The user is not a member of the DM.')

    name = dms[dm_id]['name']

    return {
        'name': name,
        'members': dms[dm_id]['all_members']
    }


def dm_leave_v1(auth_user_id, dm_id):
    '''
    Parameters:
        {auth_user_id (integer), dm_id (integer)}
    Given a DM ID, the user is removed as a member of this DM. 
    The creator is allowed to leave and the DM will still exist if this happens. 
    This does not update the name of the DM.
    InputError when:
        dm_id does not refer to a valid DM
    AccessError when:
        dm_id is valid and the authorised user is not a member of the DM
    Return Value: {}
    '''
    store = data_store.get()
    dms = store['dms']
    users = store['users']
    session_dms = store['session_dms']

    # InputError when:
    # dm_id does not refer to a valid DM
    if dm_id < 0 or dm_id >= session_dms:
        raise InputError(description='This dm does not exist')
    if dms[dm_id] is None:
        raise InputError(description='This dm has been deleted')
    # AccessError when
        # dm_id is valid and the authorised user is not a member of the DM
    if not any(member['u_id'] == auth_user_id for member in dms[dm_id]['all_members']):
        raise AccessError(description='The user is not a member of the DM.')

    user_details = helper_funcs.get_user_details(users[auth_user_id])
    dms[dm_id]['all_members'].remove(user_details)

    if any(member['u_id'] == auth_user_id for member in dms[dm_id]['owner_members']):
        dms[dm_id]['owner_members'].remove(user_details)

    store['dms'] = dms
    data_store.set(store)
    return {}


def dm_messages_v1(auth_user_id, dm_id, start):
    '''
    Arguments:
        auth_id, (integer)
        dm_id, (integer)
        start (integer)

    Exceptions:
        InputError  - dm_id does not refer to a valid DM
                    - start is greater than the total number of messages in the channel
        AccessError - Occurs when dm_id is valid and the authorised user is not a 
                    member of the DM

    Return Value:
        Returns {'messages' (list of message dictionaries), 'start' (integer), 'end' (integer)}
    '''
    

    # Given a DM with ID dm_id that the authorised user
    # is a member of, return up to 50 messages between
    # index 'start' and 'start + 50'.
    # Message with index 0 is the most recent message in the DM.
    # This function returns a new index 'end' which is the
    # value of 'start + 50', or, if this function has returned
    # the least recent messages in the DM, returns -1 in 'end'
    # to indicate there are no more messages to load after
    # this return.

    store = data_store.get()
    dms = store['dms']
    session_dms = store['session_dms']

    # InputError when any of:
    #   dm_id does not refer to a valid DM
    #   start is greater than the total number of messages in the channel

    if dm_id < 0 or dm_id >= session_dms:
        raise InputError(description='This dm does not exist.')
    if dms[dm_id] is None:
        raise InputError(description='This dm has been deleted.')

    # AccessError when:
    #   dm_id is valid and the authorised user is not a member of the DM
    if not any(member['u_id'] == auth_user_id for member in dms[dm_id]['all_members']):
        raise AccessError(description='The user is not a member of the DM.')

    index = 0
    loaded_chunk = []
    end = -1

    if start < 0:
        raise InputError(description='Start must not be a negative integer.')

    for message in dms[dm_id]['messages']:
        if index == start + 50:
            end = start + 50
            break
        elif index >= start:
            loaded_chunk.append(message)
        index += 1

    if index < start:
        raise InputError(
            description='DM index requested greater than messages in DM.')

    return {
        'messages': loaded_chunk,
        'start': start,
        'end': end
    }


def message_senddm_v1(auth_user_id, dm_id, message, message_id=-1):
    '''
    Parameters:
    - { auth_user_id (integer), dm_id (integer), message (string)}
    Send a message from authorised_user to the DM specified by dm_id. 
    Note: Each message should have it's own unique ID, i.e. no messages should share 
    an ID with another message, even if that other message is in a different channel or DM.

    InputError when any of the following:
        dm_id does not refer to a valid DM
        length of message is less than 1 or over 1000 characters
    AccessError when:
        dm_id is valid and the authorised user is not a member of the DM
    Return Value:
    - {message_id (integer)}
    '''

# # Grab channels from data_store
    store = data_store.get()
    dms = store['dms']
    session_dms = store['session_dms']
    users = store['users']

    # InputError when:
    # dm_id does not refer to a valid DM
    if dm_id < 0 or dm_id >= session_dms:
        raise InputError(description='This dm does not exist')
    if dms[dm_id] is None:
        raise InputError(description='This dm has been deleted')
    # InputError when:
        # length of message is less than 1 or over 1000 characters
    # AccessError when:
        # dm_id is valid and the authorised user is not a member of the DM
    if not any(member['u_id'] == auth_user_id for member in dms[dm_id]['all_members']):
        raise AccessError(description='The user is not a member of the DM.')
    if len(message) < 1 or len(message) > 1000:
        raise InputError(description='This message is too short or too long')

    if message_id == -1:
        message_id = helper_funcs.return_message_id()

    new_message = {
        'message_id': message_id,
        'u_id': auth_user_id,
        'message': message,
        'time_created': helper_funcs.get_timestamp(),
        'reacts': [
            {
                'react_id': 1,
                'u_ids': [],
                'is_this_user_reacted': False
            }
        ],
        'is_pinned': False
    }

    dms[dm_id]['messages'].insert(0, new_message)

    "{user_handle} tagged you in {channel/dm_id}: (first 20 characters of message including the tag)"
    # User handle from auth user id
    # Append notification to tagged user's notifications list 
    sent_handle = None
    for user in users:
        if user['u_id'] == auth_user_id:
            sent_handle = user['handle_str']
    dm_name = None
    for dm in dms:
        if dm['dm_id'] == dm_id:
            dm_name = dm['name']
    for user in users:
        handle = '@' + user['handle_str']

        if re.search(rf'{handle}', message):
            if re.search(rf'{handle}\w', message):
                continue

            if user.get('notifications') is None:
                user['notifications'] = []
            new_notif = {
                'channel_id' : -1,
                'dm_id' : dm_id,
                'notification_message' : f'{sent_handle} tagged you in {dm_name}: {message[:20]}'
            }
            user['notifications'].insert(0, new_notif)

    store['dms'] = dms
    store['users'] = users
    data_store.set(store)

    return {'message_id': message_id}
