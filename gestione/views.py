from django.shortcuts import redirect, render
from gestione.backend import parsing


def homepage(request, query=None, field=None, is_syn=False, page=1):
    if request.GET.get('query') and request.GET.get('field'):
        query = request.GET.get('query')
        field = request.GET.get('field')
    if request.GET.get('is_syn'):    
        is_syn = request.GET.get('is_syn')
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    
    is_last_page = False
    
    if is_syn == 'y':
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
        'is_last_page': is_last_page,
        'is_syn': is_syn,
        'query': query,
        'field': field,
        'page': page,
    }
    
    return render(request, 'gestione/homepage.html', context)
    