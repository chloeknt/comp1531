from flask import Flask, request, jsonify
from json import dumps, loads
from number_fun import multiply_by_two, print_message, sum_list_of_numbers, sum_iterable_of_numbers, is_in, index_of_number

APP = Flask(__name__)

@APP.route("/multiply/by/two", methods=['GET'])
def get_multiply_by_two():
    data = request.args.get('number')
    return {
        'number' : multiply_by_two(int(data))
    }

@APP.route("/print/message", methods=['GET'])
def get_print_message():
    data = request.args.get('message')
    print_message(data)
    return {}

@APP.route("/sum/list/of/numbers", methods=['GET'])
def get_list_of_numbers():
    data = request.args.get('list')
    return ({
        'sum' : sum_list_of_numbers(loads(data))
    })

@APP.route("/sum/iterable/of/numbers", methods=['GET'])
def get_sum_iterable_of_numbers():
    data = request.args.get('list')
    return ({
        'sum' : sum_iterable_of_numbers(loads(data))
    })

@APP.route("/is/in", methods=['GET'])
def get_is_in():
    needle_data = request.args.get('needle')
    haystack_data = request.args.get('haystack')
    return ({
        'bool' : is_in(loads(needle_data), loads(haystack_data))
    })

@APP.route("/index/of/number", methods=['GET'])
def get_index_of_number():
    item_data = request.args.get('item')
    numbers_data = request.args.get('numbers')
    return ({
        'index' : index_of_number(loads(item_data), loads(numbers_data))
    })

if __name__ == '__main__':
    APP.run(debug=True, port=5000)