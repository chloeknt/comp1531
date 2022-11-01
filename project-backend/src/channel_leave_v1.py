from src.error import AccessError, InputError

from src.data_store import data_store
from src.helper_functions.helpers import user_in_channel, validate_auth_user, validate_channel, id_in_channel, get_user_details

def leave_v1(auth_id, channel_id):
    validate_auth_user(auth_id)
    validate_channel(channel_id)

    store = data_store.get()
    users = store['users']
    channels = store['channels']

    if not user_in_channel(auth_id, channel_id, channels):
        raise AccessError(description='The user cannot leave a channel they have not joined')
    
    # Remove user from 'all_members' list of the channel

    user_values = get_user_details(users[auth_id])
    channels[channel_id]['all_members'].remove(user_values)

    # If a user was a channel owner, remove them from the 'owner_members' list of the channel

    if user_values in channels[channel_id]['owner_members']:
        channels[channel_id]['owner_members'].remove(user_values)