from src.data_store import data_store
from src.helper_functions.helpers import validate_auth_user

def notifications_get_v1(auth_user_id):
    '''
    Description:
        Return the user's most recent 20 notifications, 
        ordered from most recent to least recent.

    Parameters:
        auth_user_id - ID of user who is a member of the channel

    Return:
        {
            'notifications' : List of dictionaries, where each dictionary contains 
            types { channel_id, dm_id, notification_message } where channel_id is the 
            id of the channel that the event happened in, and is -1 if it is being sent 
            to a DM. dm_id is the DM that the event happened in, and is -1 if it is being 
            sent to a channel. Notification_message is a string of the following format 
            for each trigger action:
            - tagged: "{User’s handle} tagged you in {channel/DM name}: {first 20 characters of the message}"
            - reacted message: "{User’s handle} reacted to your message in {channel/DM name}" 
            - added to a channel/DM: "{User’s handle} added you to {channel/DM name}"
        }

    Changes in data_store:
        None, only reads
    '''
    read = data_store.get()
    users = read['users']
    validate_auth_user(auth_user_id)
    if users[auth_user_id].get('notifications', None) is None:
        return {
            'notifications' : []
        }

    # fetch 20 notifications between indexes and append them to the loaded_chunk list
    num_notifs = len(users[auth_user_id]['notifications'])
    if num_notifs > 20:
        loaded_chunk = users[auth_user_id]['notifications'][num_notifs - 19:] 
    else:
        loaded_chunk = users[auth_user_id]['notifications']
    return {
            'notifications' : loaded_chunk
    }

