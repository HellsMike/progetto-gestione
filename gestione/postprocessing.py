import json
import re
import ast
from collections.abc import Mapping


def json_fix():
    giallo_recipes = "giallozafferano.json"
    url = f"static/collections/{giallo_recipes}"
    f = open(url, encoding='utf8')
    collection = json.load(f)
    print(type(collection))
    print(collection[1])


def cutntrim():
    giallo_recipes = "giallozafferano.json"
    url = f"static/collections/{giallo_recipes}"
    f = open(url, encoding='utf8')
    content = f.read()

    '''la roba necessaria è la prima riga, il resto è solo di abbellimento per capirci meglio qualcosa'''
    a = content.replace('\t', '').replace('\n', '').replace('\\t', '').replace('\\n', '').replace('\\', '')\
        .replace('"', ' ').replace('{"', ' ').replace('":"', ' ').replace('"}', ' ').replace('[', '')\
        .replace(']', '').replace('   ', ' ').replace(' ,', ',').replace(',', ', ')
    f.close()

    with open('static/collections/new_giallozafferano.json', 'w', encoding='utf-8') as file:
        json.dump(a, file, ensure_ascii=False, indent=4)
    file.close()



