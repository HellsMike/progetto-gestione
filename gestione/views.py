import json
from django.shortcuts import render
from gestione.postprocessing import tokenize


def homepage(request):
    url = 'static/collections/giallozafferano.json'
        
    with open(url, encoding='utf-8') as file:
        content = json.load(file)
    print(tokenize(content[0]['preparazione']))
    return render(request, 'gestione/homepage.html')
