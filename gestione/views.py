from django.http import JsonResponse
from django.shortcuts import render
from gestione.backend import parsing


def homepage(request):
    query = request.GET.get('query')
    field = request.GET.get('field')
    is_syn = request.GET.get('enable_syn') == 'on'
    current_page = request.GET.get('current_page')
    
    if current_page:
        current_page = int(current_page)
        results = parsing(query, field, is_syn, current_page+1)
        current_page += 1
        current_results = int(request.GET.get('current_results')) + results.pagelen
        total_results = int(request.GET.get('total_results'))
        
        if current_page * 20 >= total_results:
            new_results = []
            return JsonResponse({
                'current_page': current_page,
                'results': new_results
            })
        else:
            new_results = []
            for result in results:
                new_results.append(result.fields())
            return JsonResponse({
                'current_results': current_results,
                'current_page': current_page,
                'results': new_results,
            })
    elif query not in [None, ""]:
        results = parsing(query, field, is_syn)
        current_page = 1
        total_results = len(results)
        current_results = results.pagelen
    else:
        return render(request, 'gestione/homepage.html')

    if is_syn:
        context["enable_syn"] = "on"
        
    context = {
        'current_page': current_page,
        'current_results': current_results,
        'total_results': total_results,
        'results': list(results),
        'query': query,
        'field': field,
        'enable_syn': 'on' if is_syn else ''
    }
    
    return render(request, 'gestione/homepage.html', context)
