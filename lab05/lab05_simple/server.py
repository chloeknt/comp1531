from flask import Flask, request, jsonify
from json import dumps

APP = Flask(__name__)
names_list = []

@APP.route("/names/add", methods=['POST'])
def names_add():
    global names_list
    data = request.get_json()
    names_list.append(data['name']) 
    return jsonify({})

@APP.route("/names", methods=['GET'])
def names_get():
    global names_list
    return jsonify({
        'names' : names_list
    })

@APP.route("/names/remove", methods=['DELETE'])
def names_remove():
    global names_list
    data = request.get_json()
    if data['name'] in names_list:
        names_list.remove(data['name'])
    return jsonify({})

@APP.route("/names/clear", methods=['DELETE'])
def names_clear():
    global names_list
    names_list.clear()
    return jsonify({})

if __name__ == '__main__':
    APP.run(debug=True, port=5000)