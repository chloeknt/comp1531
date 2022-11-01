import json
import operator
import pickle
from collections import Counter

def process():
    with open("shapecolour.p", "rb") as raw_data:
        data = pickle.load(raw_data)
        common = most_common()
        info = {"mostCommon" : common, "rawData" : data}
        with open("processed.json", "w", encoding = ascii) as processed:
            json.dump(info, processed)

def most_common():
    with open("shapecolour.p", "rb") as pickle_off:
        data = pickle.load(pickle_off)
        info = Counter((item['shape'], item['colour']) for item in data)
        result = info.most_common(1)[0][0]
        return {'shape': result[0], 'colour': result[1]}
