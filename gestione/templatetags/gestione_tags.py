from django import template


register = template.Library()


@register.filter
def process_ingredients(ingredients):
    return ingredients.split(', ')


@register.filter
def normalize_url(url):
    return ''.join(filter(str.isalnum, url))


@register.filter
def fancy_source(url):
    if url == 'https://www.giallozafferano.it/':
        return 'Giallo Zafferano'
    if url == 'https://ricette.donnamoderna.com/':
        return 'Donna Moderna Food'
