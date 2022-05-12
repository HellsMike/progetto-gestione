from django.shortcuts import render
from gestione.postprocessing import json_fix


def homepage(request):

    return render(request, 'gestione/homepage.html')
