from src.data_store import data_store
from src.error import InputError, AccessError

def search_v1(auth_user_id, query_str):
    '''
    Description:
        - Given a query string, return a collection of messages in all of the 
        channels/DMs that the user has joined that contain the query.
    
    Parameters: 
        auth_user_id - ID of user searching for messages
        query_str - string of characters to search messages with

    Return:
        messages - list of dictionaries, where each dictionary contains types 
        { message_id, u_id, message, time_created, reacts, is_pinned  }
    
    Exceptions:
    InputError when:
        - length of query_str is less than 1 or over 1000 characters

    Changes in data store:
        none, only reads
    '''
    store = data_store.get()
    channels = store['channels']
    dms = store['dms']

    messages = []

    if len(query_str) < 1 or len(query_str) > 1000:
        raise InputError( description = 'Query String is of an invalid length.')

    for channel in channels:
        # check user has joined the channel
        for each_member in channel['all_members']:
            if each_member['u_id'] == auth_user_id:
                for message in channel['messages']:
                    if query_str.lower() in message['message'].lower():
                        messages.append(message)

    for dm in dms:
        for each_member in dm['all_members']:
            if each_member['u_id'] == auth_user_id:
                for message in dm['messages']:
                    if query_str.lower() in message['message'].lower():
                        messages.append(message)
    
    messages = messages[::-1]

    return { 'messages': messages }