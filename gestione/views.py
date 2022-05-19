from django.shortcuts import redirect, render
from gestione.backend import parsing


def homepage(request, query=None, field=None, is_syn='nosyn', page=1):   
    is_last_page = False
    
    if query not in [None, '']:
        results = parsing(query, field, is_syn, page)
        if parsing(query, field, is_syn, page+1)[0] == results[0]:
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
  
  
def get_data(request):
    url = ''
    if request.POST.get('query') and request.POST.get('field'):
        query = request.POST.get('query')
        field = request.POST.get('field')
        url += f'/{field}/{query}'
        if request.POST.get('is_syn'):    
            is_syn = request.POST.get('is_syn')
            url += f'/{is_syn}'
        if request.POST.get('page'):
            page = int(request.POST.get('page'))
            url += f'/{page}'
    if url == '':
        return redirect('/')
    
    return redirect(url)
