import pickle

'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

# Opening lines - Import a copy of the store to work on within your function
    from data_store import data_store

    For editing the data_store use:
        store = data_store.get()
    
    For reading the data_store use:
        read = data_store.get()

# Depending on the aspects you want to work on, create copies of the variables
    users = store['users']
    channels = store['channels']
    dms = store['dms']
    session_users = store['session_users']
    session_channels = store['session_channels']
    session_dms = store['session_dms']
    session_messages = store['session_messages']

# Structure of a user

    # active_tokens (added in iteration v2)
        List of tokens for each active user session (multiple logins on different
        devices) to ensure that we can verify each user session.
        Each token is unique as it also encodes the 'total_session_ids' variable.

    example_user = {
        'u_id' = 123, # User id number should be derived by incrementing store['session_users']
        'email' = 'string',
        'name_first' = 'string',
        'name_last' = 'string',
        'handle_str' = 'string',
        'password' = 'string',
        'permission_id' = 1, # Number 1 for owner, 2 for member
        'active_tokens' = [list of tokens],
        'user_stats': {
            'channels_joined' = [{'num_channels_joined' = 0, timestamp}, ...]
            'dms_joined' = [{'num_dms_joined' = 0, timestamp}, ...],
            'msgs_sent' = [{'num_msgs_sent' = 0, timestamp}, ...],
            'involvement_rate' = 0
        }
        'permission_id' = 1 # Number 1 for owner, 2 for member
        'active_tokens' = [list of tokens] 
        'notifications' = [list of notifications]
    }

    # Creating/Modifying a user
        To create, you can pass values into the block directly as above.
        Then you MUST append the user to the users list to save it.

        E.g. users.append(example_user)

        To modify, access the user by user_id, then access the value by key.
        Make sure to use the same data type as it should be.

        E.g. users[user_id]['private_channels'] = [channel1, channel2]
             users[user_id]['email'] = 'new@email.com'

    # Deleting a user
        We are using a 'soft' delete approach to ensure user ids map to index in users list
        To delete, set the relevant index to None.

        E.g. users[user_id] = None

    # Accessing user data
        Access the user by user_id, then access the value by key.

# Structure of a channel

    example_channel = {
        'channel_id' = 123, # User id number should be derived by incrementing store['session_channels']
        'name' = 'string',
        'is_public' = True / False,
        'owner_members' = [{user}] ## {user} only contains u_id, email, name_first, name_last and handle_str
        'all_members' = [{user}]
        'messages' = [list of message objects]
        'standup_info' = {'user', 'is_active', 'time_finish', 'queue'}
    }

    # Creating/Modifying a channel
        To create, you can pass values into the block directly as above.
        Then you MUST append the channel to the channels list to save it.

        E.g. channels.append(example_channel)

        To modify, access the channel by channel_id, then access the value by key.
        Make sure to use the same data type as it should be.

        E.g. channels[channel_id]['messages'] = [{message object 1}, {message object 2}]
             channels[channel_id]['is_public'] = True

    # Deleting a channel
        We are using a 'soft' delete approach to ensure channel ids map to index in channels list
        To delete, set the relevant index to None.

        E.g. channels[channel_id] = None

    # Accessing channel data
        Access the channel by channel_id, then access the value by key.

# Structure of a dm

    example_dm = {
        'dm_id' = 123, # User id number should be derived by incrementing store['session_dms']
        'name' = 'string',
        'is_public' = True / False,
        'owner_members' = [{user}] ## {user} only contains u_id, email, name_first, name_last and handle_str
        'all_members' = [{user}]
        'messages' = [list of message objects]
    }

    # Creating/Modifying a dm
        To create, you can pass values into the block directly as above.
        Then you MUST append the dm to the dms list to save it.

        E.g. dms.append(example_dm)

        To modify, access the dm by dm_id, then access the value by key.
        Make sure to use the same data type as it should be.

        E.g. dms[dm_id]['messages'] = [{message object 1}, {message object 2}]

    # Deleting a dm
        We are using a 'soft' delete approach to ensure dm ids map to index in dms list
        To delete, set the relevant index to None.

        E.g. dms[dm_id] = None

    # Accessing dm data
        Access the dm by dm_id, then access the value by key.

# Structure of a message

    example_message = {
        'message_id': 1,
        'u_id' = user_id,
        'message' = 'string',
        'time_created' = unix timestamp(of type int), # See how to use here https://www.tutorialspoint.com/How-to-convert-Python-date-to-Unix-timestamp
    }

# Closing lines - before exiting your function you must save the data back into the datastore object
    store['users'] = users
    store['channels'] = channels
    store['dms'] = dms
    store['session_users'] = session_users
    store['session_channels'] = session_channels
    store['session_dms'] = session_dms
    store['session_messages'] = session_messages
    data_store.set(store)
'''

# YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    'channels': [],
    'dms': [],
    'session_users': 0,
    'session_channels': 0,
    'session_dms': 0,
    'session_messages': 0,
    'total_session_ids': 0,
    'workspace_stats': {
        'channels_exist': [],
        'dms_exist': [],
        'messages_exist': [],
        'utilization_rate': 0.0
    }
}
# YOU SHOULD MODIFY THIS OBJECT ABOVE


class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def save_data_to_file(self):
        ''' 
        Save the data store as a pickled file ready to be decoded in case the 
        server shuts down.
        '''
        store = self.get()

        # file 1: users - contains a list of dictionaries
        # [{user}, {user}]
        # file 2: channels - contains a list of dictionaries
        # [{channel}, {channel}]
        # file 3: session users and session channels - dictionary of integers
        # {'session_users': int, 'session_channels': int, 'session_dms': int, 'total_session_ids': int, 'workspace_stats': dict}

        with open('saved_users_data.p', 'wb') as pickle_on_users:
            users = store['users']
            pickle.dump(users, pickle_on_users)

        with open('saved_channels_data.p', 'wb') as pickle_on_channels:
            channels = store['channels']
            pickle.dump(channels, pickle_on_channels)

        with open('saved_session_data.p', 'wb') as pickle_on_session:
            session_users = store['session_users']
            session_channels = store['session_channels']
            session_dms = store['session_dms']
            total_session_ids = store['total_session_ids']
            workspace_stats = store['workspace_stats']
            info = {'session_users': session_users,
                    'session_channels': session_channels,
                    'session_dms': session_dms,
                    'total_session_ids': total_session_ids,
                    'workspace_stats': workspace_stats}
            pickle.dump(info, pickle_on_session)

    def read_data_from_file(self):
        ''' 
        Load the data store as an unpickled file into data store once the server
        restarts.
        '''
        store = self.get()
        try:
            with open('saved_users_data.p', 'rb') as pickle_off_users:
                users_data = pickle.load(pickle_off_users)
                store['users'] = users_data
        except FileNotFoundError:
            print('No saved users data file detected. Please ensure file is server root directory and named "saved_users_data.p"')

        try:
            with open('saved_channels_data.p', 'rb') as pickle_off_channels:
                channels_data = pickle.load(pickle_off_channels)
                store['channels'] = channels_data
        except FileNotFoundError:
            print('No saved channels data file detected. Please ensure file is server root directory and named "saved_channels_data.p"')

        try:
            with open('saved_session_data.p', 'rb') as pickle_off_users:
                sessions_data = pickle.load(pickle_off_users)
                store['session_users'] = sessions_data['session_users']
                store['session_channels'] = sessions_data['session_channels']
                store['session_dms'] = sessions_data['session_dms']
                store['total_session_ids'] = sessions_data['total_session_ids']
                # store['workspace_stats'] = sessions_data['workspace_stats']
        except FileNotFoundError:
            print('No saved session data file detected. Please ensure file is server root directory and named "saved_session_data.p"')

        self.set(store)

    def set(self, store):
        self.save_data_to_file()
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store


print('Loading Datastore...')

global data_store
data_store = Datastore()
data_store.read_data_from_file()
