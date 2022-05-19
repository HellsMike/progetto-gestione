from django import template


register = template.Library()


@register.filter
def process_ingredients(ingredients):
    return ingredients.split(', ')


@register.filter
def normalize_url(url):
    return ''.join(filter(str.isalnum, url))
