import json
import os
from django.conf import settings

def load_json_data():
    "C:\\Users\\t_oka\\Desktop\\hackz\\app\\date\\trusty-coder-436713-n0-bbe31e8f6af0.json" = os.path.join(settings.DATA_DIR, 'trusty-coder-436713-n0-bbe31e8f6af0.json')
    with open("C:\\Users\\t_oka\\Desktop\\hackz\\app\\date\\trusty-coder-436713-n0-bbe31e8f6af0.json") as json_file:
        data = json.load(json_file)
    return data