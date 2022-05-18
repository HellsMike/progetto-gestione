from django.shortcuts import redirect, render
from gestione.backend import parsing


def homepage(request, query=None, field=None, is_syn=False, page=1):   
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
        'is_last_page': is_last_page
    }
    
    return render(request, 'gestione/homepage.html', context)


def get_query(request):
    query = request.GET.get('query')
    field = request.GET.get('field')
    is_syn = request.GET.get('is_syn')
    page = request.GET.get('page')
    
    return redirect(f'homepage/{query}/{field}/{is_syn}/{page}')
