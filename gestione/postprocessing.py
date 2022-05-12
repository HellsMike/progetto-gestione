from encodings import utf_8
import json


def json_fix():
    giallo_recipes = "giallozafferano.json"
    url = f"static/collections/{giallo_recipes}"
    f = open(url, encoding='utf8')
    collection = json.load(f)
    print(type(collection))
    print(collection[1])