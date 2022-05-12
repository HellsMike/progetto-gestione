from django.shortcuts import render
from gestione.postprocessing import json_fix


def homepage(request):
    json_fix()
    return render(request, 'gestione/homepage.html')
