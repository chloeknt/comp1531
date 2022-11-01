from src.data_store import data_store
from src.error import AccessError, InputError
from src.helper_functions.helpers import validate_u_id, return_global_owners, get_messages, msg_search_and_replace


def permission_change_v1(auth_id, u_id, permission_id):
    '''
    Arguments:
        auth_id, (integer)
        u_id, (integer)
        permission_id (integer)

    Exceptions:
        InputError  - Occurs when u_id is not a valid user, u_id refers too a user who is
                    the only global owner and they are being demoted to a user, permision_id
                    is invalid
        AccessError - Occurs when the authorised user is not a global owner

    Return Value:
        Returns {}
    '''

    store = data_store.get()
    users = store['users']

    if users[auth_id]['permission_id'] != 1:
        raise AccessError( description ='The authorised user is not a global owner!')

    validate_u_id(u_id)

    global_owner_count = return_global_owners(users)

    if not permission_id in [1, 2]:
        raise InputError( description =
            'Please enter a valid permission_id. 1 for owner, 2 for member')

    if global_owner_count == 1 and auth_id == u_id and permission_id == 2:
        raise InputError( description ='The only global user left cannot be demoted')

    users[u_id]['permission_id'] = permission_id

    store['users'] = users
    data_store.set(store)


def user_remove_v1(auth_id, u_id):
    '''
    Arguments:
        auth_id, (integer)
        u_id, (integer)

    Exceptions:
        InputError  - Occurs when u_id does not refer to a valid user
                    u_id refers to a user who is the only global owner
        AccessError - the authorised user is not a global owner

    Return Value:
        Returns {}
    '''

    store = data_store.get()
    users = store['users']
    channels = store['channels']
    dms = store['dms']

    if users[auth_id]['permission_id'] != 1:
        raise AccessError( description ='The authorised user is not a global owner!')

    validate_u_id(u_id)

    global_owner_count = return_global_owners(users)

    if global_owner_count == 1 and users[u_id]['permission_id'] == 1:
        raise InputError( description ='Cannot remove the only global owner')
    else:
        users[u_id]['name_first'] = 'Removed'
        users[u_id]['name_last'] = 'user'
        users[u_id]['handle_str'] = ''
        users[u_id]['email'] = ''
        message_ids = get_messages(u_id)

        for msg_id in message_ids:
            msg_search_and_replace(u_id, msg_id, 'Removed user')

    for channel in channels:
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                channel['all_members'].remove(member)
        for member in channel['owner_members']:
            if member['u_id'] == u_id:
                channel['owner_members'].remove(member)
            
    for dm in dms:
        for member in dm['all_members']:
            if member['u_id'] == u_id:
                dm['all_members'].remove(member)
        for member in dm['owner_members']:
            if member['u_id'] == u_id:
                dm['owner_members'].remove(member)    

    store['channels'] = channels
    store['dms'] = dms
    store['users'] = users
    data_store.set(store)

    return {}
