'''
users.py - COMP1531 Team T09 Dodo
    Description:
        Implements functionality regarding user information for UNSW Streams
'''

from src.data_store import data_store
from src.error import InputError
from src.helper_functions.auth_helpers import validate_email, validate_name
from src.helper_functions.helpers import active, validate_u_id, get_user_details, get_timestamp, get_messages, get_num_users_in_channel_or_dm
from src.helper_functions.auth_helpers import validate_name, validate_email, does_handle_exist
from src.iter1.channels_v1 import channels_list_v1, channels_listall_v1
from src.dm import dm_list_v1

def users_all_v1():
    ''' 
    Returns a list of all users and their associated details.
    
    Exceptions:
    N/A

    Return Type:
    {'users': List of dictionaries of type user}
    user type: {u_id, email, name_first, name_last, handle_str}
    '''

    store = data_store.get()
    users_list = store['users']

    users_details = []

    for user in active(users_list):
        if user['name_first'] != 'Removed' and user['name_last'] != 'user':
            users_details.append(get_user_details(user))

    return {
        'users': users_details
    }

def user_profile_v1(u_id):
    '''
    For a valid user, returns information about their user_id, email, first name, last name, and handle
    
    Exceptions:
    InputError when:
        u_id does not refer to a valid user
    
    Return Type:
    {'user': Dictionary of type user}
    user type: {u_id, email, name_first, name_last, handle_str}
    '''

    store = data_store.get()
    users_list = store['users']
    session_users = store['session_users']

    # check for valid u_id and raise an Input Error if invalid
    if u_id < 0 or u_id >= session_users:
        raise InputError(description='This user has not been registered')

    return {
        'user' : get_user_details(users_list[u_id])
    }

def user_profile_setname_v1(auth_user_id, name_first, name_last):
    '''
    Update the authorised user's first and last name
    
    Exceptions:
    InputError when:
        length of name_first is not between 1 and 50 characters inclusive
        length of name_last is not between 1 and 50 characters inclusive
    
    Return Type:
    {}
    '''

    store = data_store.get()
    users_list = store['users']

    if name_first == 'Removed' and name_last == 'user':
        raise InputError(description='Invalid name type, please try something besides "Removed user"')

    # check first and last names are between 1 and 50 characters
    validate_name(name_first, 'first')
    validate_name(name_last, 'last')

    # get a user id using the auth_user_id
    user = users_list[auth_user_id]
    user['name_first'] = name_first
    user['name_last'] = name_last
    data_store.set(store)

    return {}

def user_profile_setemail_v1(auth_user_id, email):
    '''
    Update the authorised user's email address
    
    Exceptions:
    InputError when:
        email entered is not a valid email (more in section 6.4)
        email address is already being used by another user
    
    Return Type:
    {}
    '''

    store = data_store.get()
    users_list = store['users']

    # Validate email
    validate_email(email, users_list)

    user = users_list[auth_user_id]
    user['email'] = email.lower()
    data_store.set(store)

    return {}

def user_profile_sethandle_v1(auth_user_id, handle_str):
    '''
    Update the authorised user's email address
    
    Exceptions:
    InputError when any of:
        length of handle_str is not between 3 and 20 characters inclusive
        handle_str contains characters that are not alphanumeric
        the handle is already used by another user

    Return Type:
    {}
    '''

    store = data_store.get()
    users_list = store['users']

    # check if handle is of correct length
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description='The handle must be between 3 and 20 characters long (inclusive)')

    # check if handle is already in use
    if does_handle_exist(handle_str, users_list):
        raise InputError(description='This handle is taken')

    # check all characters in handle are alpha-numeric
    if handle_str.isalnum() == False:
        raise InputError(description='Handle string must contain only alphanumeric characters')

    user = users_list[auth_user_id]
    user['handle_str'] = handle_str
    store['users'] = users_list
    data_store.set(store)

    return {}

def user_stats_v1(auth_user_id):
    """ 
    Fetch required statistics about this user's use of UNSW Streams.

    Parameters:
        auth user id

    Exceptions:
        N/A
    
    Return Type:
        {'user_stats': 
            {
                channels_joined: [{num_channels_joined, time_stamp}],
                dms_joined: [{num_dms_joined, time_stamp}], 
                messages_sent: [{num_messages_sent, time_stamp}], 
                involvement_rate
            }
        }
    """

    store = data_store.get()
    users_list = store['users']
    session_dms = store['session_dms']
    session_messages = store['session_messages']
    
    # set all stats to 0
    num_channels_joined = 0
    num_dms_joined = 0
    num_msgs_sent = 0
    num_channels_total = 0
    num_dms_total = session_dms
    num_msgs_total = session_messages

    # number of channels user is in
    num_channels_joined = len(channels_list_v1(auth_user_id)['channels'])
    # number of dms user is in
    num_dms_joined = len(dm_list_v1(auth_user_id))
    # number of messages user has sent
    num_msgs_sent = len(get_messages(auth_user_id))

    # number total channels
    num_channels_total = len(channels_listall_v1(auth_user_id)['channels'])
    # channels_list = channels_listall_v1(auth_user_id)['channels']
    # for i in range(len(channels_list)):
    #     if channels_list[i] != None:
    #         num_channels_total += 1

    # calculate involvement rate
    involvement_rate = 0
    if (num_channels_total + num_dms_total + num_msgs_total) != 0:
        involvement_rate = (num_channels_joined + num_dms_joined + num_msgs_sent)/(num_channels_total + num_dms_total + num_msgs_total)
        if involvement_rate > 1:
            involvement_rate = 1

    # update user stats in data store
    cur_timestamp = get_timestamp()

    # check if user_stats exists in datastore
    user = users_list[auth_user_id]
    if user.get('user_stats') == None:
        user_stats = {
            'channels_joined': [{'num_channels_joined': num_channels_joined, 'time_stamp': cur_timestamp}],
            'dms_joined': [{'num_dms_joined': num_dms_joined, 'time_stamp': cur_timestamp}],
            'messages_sent': [{'num_messages_sent': num_msgs_sent, 'time_stamp': cur_timestamp}],
            'involvement_rate': float(involvement_rate)
        }
        user['user_stats'] = user_stats
    else:
        current_stats = user['user_stats']

        # update channels stats
        if num_channels_joined != current_stats['channels_joined'][-1]['num_channels_joined']:
            channels_joined_new_dict = {'num_channels_joined' : num_channels_joined, 'time_stamp': cur_timestamp}
            current_stats['channels_joined'].append(channels_joined_new_dict)

        # update dms stats
        if num_dms_joined != current_stats['dms_joined'][-1]['num_dms_joined']:
            dms_joined_new_dict = {'num_dms_joined': num_dms_joined, 'time_stamp': cur_timestamp}
            current_stats['dms_joined'].append(dms_joined_new_dict)

        # update messages stats
        if num_msgs_sent >  current_stats['messages_sent'][-1]['num_messages_sent']:
            msgs_sent_new_dict = {'num_messages_sent': num_msgs_sent, 'time_stamp': cur_timestamp}
            current_stats['messages_sent'].append(msgs_sent_new_dict)

        # update involvment rate stats
        current_stats['involvement_rate'] = float(involvement_rate)

    store['users'] = users_list
    data_store.set(store)
    
    return {'user_stats': user['user_stats']}

def workspace_stats_v1(auth_user_id):
    """ 
    Fetch required statistics about the use of UNSW Streams.

    Exceptions:
        N/A
    
    Return Type:
        {'workspace_stats': 
            {
                channels_exist: [{num_channels_exist, time_stamp}], 
                dms_exist: [{num_dms_exist, time_stamp}], 
                messages_exist: [{num_messages_exist, time_stamp}], 
                utilization_rate
            }
        }
    """

    store = data_store.get()
    users_list = store['users']
    current_stats = store['workspace_stats']
    session_dms = store['session_dms']
    session_messages = store['session_messages']

    # set all stats to 0
    num_channels_total = 0
    num_dms_total = session_dms
    num_msgs_total = session_messages

    # number total channels
    num_channels_total = len(channels_listall_v1(auth_user_id)['channels'])

    # calculate utilization rate
    num_users_in_channel_or_dm = get_num_users_in_channel_or_dm(auth_user_id)
    num_users = len(users_list)

    utilization_rate = float(num_users_in_channel_or_dm/num_users)

    # update user stats in data store
    cur_timestamp = get_timestamp()

    # check if workspace_stats changed in datastore
    if current_stats['channels_exist'] == [] or (current_stats['channels_exist'][-1]['num_channels_exist'] != num_channels_total):
        channels_total_new_dict = {'num_channels_exist' : num_channels_total, 'time_stamp': cur_timestamp}
        current_stats['channels_exist'].append(channels_total_new_dict)
    
    if len(current_stats['dms_exist']) != num_dms_total:
        dms_total_new_dict = {'num_dms_exist': num_dms_total, 'time_stamp': cur_timestamp}
        current_stats['dms_exist'].append(dms_total_new_dict)
    elif current_stats['dms_exist'] != []:
        if current_stats['dms_exist'][-1]['num_dms_exist'] != num_dms_total:
            dms_total_new_dict = {'num_dms_exist': num_dms_total, 'time_stamp': cur_timestamp}
            current_stats['dms_exist'].append(dms_total_new_dict)

    if len(current_stats['messages_exist']) != num_msgs_total:
        messages_total_new_dict = {'num_messages_exist': num_msgs_total, 'time_stamp': cur_timestamp}
        current_stats['messages_exist'].append(messages_total_new_dict)
    elif current_stats['messages_exist'] != []:
        if current_stats['messages_exist'][-1]['num_messages_exist'] != num_msgs_total:
            messages_total_new_dict = {'num_messages_exist': num_msgs_total, 'time_stamp': cur_timestamp}
            current_stats['messages_exist'].append(messages_total_new_dict)

    current_stats['utilization_rate'] = utilization_rate

    store['workspace_stats'] = current_stats
    data_store.set(store)

    return {'workspace_stats': store['workspace_stats']}