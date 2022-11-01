'''
auth.py - COMP1531 Team T09 Dodo
    Description:
        Implements user login and registration functionality for UNSW Streams
'''

from src.data_store import data_store
from src.error import InputError
from src.helper_functions.auth_helpers import validate_email, validate_name,\
                             validate_password, create_handle, generate_code
import src.helper_functions.helpers as helper_fns
import smtplib
from email.message import EmailMessage
import hashlib
import time
from src.config import url

def auth_login_v1(email, password):
    '''
    Description:
        Given a registered user's valid email and password,
        returns their `auth_user_id` value.

    Parameters:
        email - user email as string
        password - user password as string

    Return:
        {'auth_user_id': id} - Dictionary containing 'auth_user_id' int

    Changes in data_store:
        None, only reads

    InputError when any of:
        email entered does not belong to a user
        password does not match the given user
    '''

    # Setup data_store access
    read = data_store.get()
    users = read['users']

    # email MUST be stored in lowercase to avoid confusion in other functions
    email = email.lower()

    # check to ensure fields are not empty
    if email == '' or password == '':
        raise InputError( description='Empty fields are not allowed.')

    for user in helper_fns.active(users):
        if user['email'] == email:
            if user['password'] == password:
                return {'auth_user_id': user['u_id']}
            raise InputError( description='Incorrect password.')
    raise InputError( description='Unregistered email. No user with this email exists.')


def auth_register_v1(email, password, name_first, name_last):
    '''
    Description:
        Registers a new user into the data store,
        if the input fields are valid.

    Parameters:
        email - user email as string
        password - user password as string
        name_first - user's firstname as string
        name_last - user's lastname as string

    Return:
        {'auth_user_id': id} - Dictionary containing 'auth_user_id' int

    Changes in data_store:
        increments session_users
        appends to users list

    The helper functions may raise InputError when any of:
        inputs are not of the type string
        inputs are empty
        inputs are of an invalid format
    '''

    # Setup data_store access
    store = data_store.get()
    users = store['users']
    session_users = store['session_users']

    # remove leading and trailing white space
    # email must be stored as lowercase
    email = email.strip().lower()
    name_first = name_first.strip()
    name_last = name_last.strip()

    # check the validity of the inputs
    validate_email(email, users)
    validate_name(name_first, 'First')
    validate_name(name_last, 'Last')

    if name_first == 'Removed' and name_last == 'user':
        raise InputError(description='Invalid name type, please try something besides "Removed user"')

    given_name = (name_first + name_last).lower()

    # create a new account with all fields populated
    new_account = {
        'u_id': session_users,
        'email': email,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': create_handle(given_name, users),
        'profile_img_url': f'{url}imgurl/default.jpg',
        'password': password,
        'notifications': [],
        'permission_id': 2,  # Default value of member. Changed if account id == 0
        'reset_code': None
    }

    if new_account['u_id'] == 0:
        new_account['permission_id'] = 1

    # add user to list of users
    users.append(new_account)
    session_users += 1

    # Get timestamp for User_stats, Workspace_stats initialization
    cur_timestamp = helper_fns.get_timestamp()

    # User_stats initialize:
    auth_user_id = new_account['u_id']
    user = users[auth_user_id]

    user['user_stats'] = {
        'channels_joined': [{'num_channels_joined': 0, 'time_stamp': cur_timestamp}],
        'dms_joined': [{'num_dms_joined': 0, 'time_stamp': cur_timestamp}],
        'messages_sent': [{'num_messages_sent': 0, 'time_stamp': cur_timestamp}],
        'involvement_rate': 0
    }

    # Workspace_stats initialize if first user:
    current_stats = store['workspace_stats']
    if len(users) == 1:
        channels_intialise_dict = {'num_channels_exist' : 0, 'time_stamp': cur_timestamp}
        current_stats['channels_exist'].append(channels_intialise_dict)
        
        dms_intialise_dict = {'num_dms_exist': 0, 'time_stamp': cur_timestamp}
        current_stats['dms_exist'].append(dms_intialise_dict)

        messages_total_new_dict = {'num_messages_exist': 0, 'time_stamp': cur_timestamp}
        current_stats['messages_exist'].append(messages_total_new_dict)

        current_stats['utilization_rate'] = 0

    store['users'] = users
    store['workspace_stats'] = current_stats
    store['session_users'] = session_users
    data_store.set(store)

    # return a new 'auth_user_id'
    return {'auth_user_id': new_account['u_id']}

def auth_passwordreset_request_v1(email):
    '''
    Description:
        Given an email address, if the user is a registered user, sends them an email containing 
        a specific secret code, that when entered in auth/passwordreset/reset, shows that the user 
        trying to reset the password is the one who got sent this email. No error should be raised 
        when passed an invalid email, as that would pose a security/privacy concern. 
        When a user requests a password reset, they should be logged out of all current sessions.

    Parameters:
        email - user email as string
    
    InputError or AccessError:
        N/A.

    Return:
        {}

    Changes in data_store:
        adds code to users
    '''
    store = data_store.get()
    users = store['users']

    reset_code = generate_code(email + str(time.time))

    email_valid = False

    for user in users:
        if user is not None:
            if user['email'] == email:
                user['reset_code'] = reset_code
                email_valid = True
    
    if email_valid == False:
        return None
    
    sender_email = 'dodot09atestsenderemail@gmail.com'
    password = 'dodotestemail123'

    msg = EmailMessage()
    msg['Subject'] = 'Test!'
    msg['From'] = sender_email
    msg['To'] = email
    msg.set_content(reset_code)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)
    
    store['users'] = users
    data_store.set(store)

def auth_passwordreset_reset_v1(reset_code, new_password):
    '''
    Description:
        Given a reset code for a user, set that user's new password to the password provided.

    Parameters:
        reset_code - code as string
        new_password - user password as string

    Return:
        {}

    Changes in data_store:
        changes password

    InputError when any of:
        - reset_code is not a valid reset code
        - password entered is less than 6 characters long
    '''

    store = data_store.get()
    users = store['users']

    valid_reset = False

    for user in users:
        if user is not None:
            if user['reset_code'] == reset_code:
                user['reset_code'] = None
                validate_password(new_password)
                user['password'] = hashlib.sha256(new_password.encode()).hexdigest()
                valid_reset = True

    if valid_reset is False:
        raise InputError(description="The reset code given is incorrect.")

    store['users'] = users
    data_store.set(store)
