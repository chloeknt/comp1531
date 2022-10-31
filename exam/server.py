'''
The flask server wrapper

All endpoints return JSON as output.
All POST requests pass parameters through JSON instead of Form.
'''
from json import dumps
from flask import Flask, request
from config import port

import trouble

APP = Flask(__name__)

'''
Endpoint: '/clear'
Method: POST
Parameters: {}
Output: {}

Resets the state of the server. Please implement this as we use it during marking.
'''
@APP.route("/clear", methods=['POST'])
def post_clear():
    clear()
    return jsonify({})

'''
Endpoint: '/flip_card'
Method: POST
Parameters: {"suit": String, "number": Integer}
Output: {}

Calls the underlying flip card function to implement it's behaviour
'''
@APP.route("/flip_card", methods=['POST'])
def post_flip_card():
    data = request.get_json()
    info = {"suit": data['Suit'], "number": data["Integer"]}
    flip_card(info)
    return jsonify({})
'''
Endpoint: '/is_double_trouble'
Method: GET
Parameters: {}
Output: { "result": Boolean }

Returns true if the last two cards were the same number. False otherwise.
If this function is called whilst true, the pile is reset to empty.
'''
@APP.route("/is_double_trouble", methods=['GET'])
def get_double_trouble():
    return jsonify({
        "result" : is_double_trouble()
    })
'''
Endpoint: '/is_trouble_double'
Method: GET
Parameters: {}
Output: { "result": Boolean }

Returns true if the last four cards had the same suit. False otherwise.
If this function is called whilst true, the pile is reset to empty.
'''
@APP.route("/is_trouble_double", methods=['GET'])
def get_trouble_double():
    return jsonify({
        "result" : is_trouble_double()
    })
'''
Endpoint: '/is_empty'
Method: GET
Parameters: {}
Output: { "result": Boolean }

Returns a boolean that is true if the pile of cards is empty, false if it is not empty
'''
@APP.route("/is_empty", methods=['GET'])
def get_is_empty():
    return jsonify({
        "result" : is_empty()
    })


if __name__ == '__main__':
    APP.run(debug=True, port=port)
