'''
other.py - COMP1531 Team T09 Dodo
    Description:
        Functions that provide additional functionality
'''

from src.data_store import data_store


def clear_v1():
    '''
    Description:
        Clears all values in the data_store.

    Parameters:
        None

    Return:
        {} - Empty dictionary

    Changes in data_store:
        resets values of session_users and session_channels to 0
        resets values of users and channels to empty lists
    '''

    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['session_users'] = 0
    store['session_channels'] = 0
    store['session_messages'] = 0
    data_store.set(store)

    return {}
