import pickle 
from collections import Counter

def most_common():
    with open("shapecolour.p", "rb") as pickle_off:
        data = pickle.load(pickle_off)
        info = Counter((item['shape'], item['colour']) for item in data)
        result = info.most_common(1)[0][0]
        print({'shape': result[0], 'colour': result[1]})
