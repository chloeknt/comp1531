'''
error.py - COMP1531 Team T09 Dodo
    Description:
        Stores error classes unique to UNSW Streams
'''

from flask import json 
from werkzeug.exceptions import HTTPException 

class AccessError(HTTPException):
    code = 403
    message = 'No message specified'

class InputError(HTTPException):
    code = 400
    message = 'No message specified'
