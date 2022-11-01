from json import dumps
from flask import Flask, Blueprint, request
from src.search import search_v1
from src.tokens import token_to_id

search = Blueprint('search',__name__)

@search.route('/search/v1', methods=['GET'])
def get_search():
    # token
    token = request.args.get('token')
    auth_user_id = token_to_id(token)
    query_str = request.args.get('query_str')

    return dumps(
        search_v1(auth_user_id, query_str)
    )