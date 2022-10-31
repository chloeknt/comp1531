'''
The flask server wrapper for the lecture question asking service.

All endpoints return JSON as output.
'''
from json import dumps
from flask import Flask, request

import questions

APP = Flask(__name__)

# Endpoint: '/question/submit'
# Verb: POST
# Parameter: (question : string)
# Output: { success : boolean, id : number}
#
# Submit the given question. The success output should be true if the question
# was successfully posted and false otherwise. If success is true then id should
# be a valid question id.

# Write this endpoint here


# Endpoint: '/questions'
# Verb: GET
# Parameter: ()
# Output: [ { id : integer, question : string, likes : integer } ]
#
# List all questions that have been submitted. The ordering of the questions is
# the same as defined in the backend.

# Write the endpoint here


# Endpoint: '/question/like'
# Verb: POST
# Parameter: (id : integer)
# Output: { success : boolean }
#
# Like question with the given id. The success output should be true if the id
# was a valid question id and false otherwise.

# Write the endpoint here


# Endpoint: '/question/dismiss'
# Verb: POST
# Parameter: (id : integer)
# Output: { success : boolean }
#
# Dismiss the question with the given id. The success output should be true if
# the id was a valid question id and false otherwise.

# Write the endpoint here


if __name__ == '__main__':
    APP.run()
