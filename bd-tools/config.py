import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
f = os.path.join(dir_path,'config.json')

try:
    with open(f) as config_file:
        data = config_file.read()
    data = json.loads(data)
except:
    print('** cannot read config.json **')
    data = {}


class env:
    @staticmethod
    def get(key):
        val = data.get(key)
        if val:
            return str(val)

