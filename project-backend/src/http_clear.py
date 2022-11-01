from json import dumps
from flask import Flask, Blueprint
from src.config import IMGURL_DIR
from src.iter1.other import clear_v1
from src.data_store import data_store
import os
import glob

clear = Blueprint('clear',__name__)

@clear.route('/clear/v1', methods=['DELETE'])
def delete_clear_v1():
    clear_v1()

    store = data_store.get()
    store['total_session_ids'] = 0
    store['users'] = []
    store['channels'] = []
    store['dms'] = []
    store['session_users'] = 0
    store['session_channels'] = 0
    store['session_dms'] = 0
    store['workspace'] = {
        'channels_exist': [],
        'dms_exist': [],
        'messages_exist': [],
        'utilization_rate': 0
    }
    data_store.set(store)

    # Clear additional user profile images

    old_user_images = glob.glob(IMGURL_DIR + '/*.jpg')
    old_user_images.remove(f'{IMGURL_DIR}/default.jpg')

    for file in old_user_images:
        try:
            os.remove(file)
        except:
            print('Error while deleting file : ', file)

    return dumps({})