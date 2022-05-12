from django.shortcuts import render
from gestione.postprocessing import json_fix, cutntrim


def homepage(request):
    json_fix()
    cutntrim()
    return render(request, 'gestione/homepage.html')
