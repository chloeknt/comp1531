'''
auth_helpers.py - COMP1531 Team T09 Dodo
    Description:
        Helper functions for auth functions
'''

''' regular expressions module allows pattern matching '''




import re
from src.error import InputError
import hashlib

def validate_email(email, users):
    ''' helper function checks if email is valid '''
    if email == '':
        raise InputError('Email cannot be empty.')

    if re.sub(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', '', email) != '':
        raise InputError('This email has an invalid format.')
    
    for user in users:
        if email == user['email']:
            raise InputError('This email has already been used.')


def validate_name(name, part):
    ''' helper function checks if names are valid '''
    if len(name) < 1:
        raise InputError(f'{part}name has too few characters.')
    if len(name) > 50:
        raise InputError(f'{part}name has too many characters.')


def validate_password(password):
    ''' helper function checks if password is valid '''
    if len(password) < 6:
        raise InputError('Password has too few characters.')


def does_handle_exist(handle, users):
    ''' helper function searched for handle '''
    for user in users:
        if user['handle_str'] == handle:
            return True
    return False


def create_handle(unfiltered_handle, users):
    ''' helper function creates the handle '''
    # parse strings and size to 20 characters
    handle = (re.sub(r'[^a-zA-Z0-9]', '', unfiltered_handle)).lower()
    maximum = 20

    if len(handle) > maximum:
        handle = handle[:maximum]

    # search for handle to see if it exists
    insert_num = 0
    original_handle = handle
    while does_handle_exist(handle, users):
        handle = original_handle + str(insert_num)
        insert_num += 1
    return handle

def generate_code(unhashed_code):
    return hashlib.sha256(unhashed_code.encode()).hexdigest()
