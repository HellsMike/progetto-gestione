from django.shortcuts import render
from django.core.paginator import Paginator
from gestione.backend import parsing


def homepage(request, query=None, field=None, is_syn=None, page=1):
    is_last_page = False
    
    if is_syn:
        is_syn = True
    if query not in [None, '']:
        results = parsing(query, field, is_syn, page)
        if len(parsing(query, field, is_syn, page+1)) < 1:
            is_last_page = True        
    else:
        results = []
        
    context = {
        'results': results,
        'is_first_page': True if page == 1 else False,
        'is_last_page': is_last_page
    }
    
    return render(request, 'gestione/homepage.html', context)
