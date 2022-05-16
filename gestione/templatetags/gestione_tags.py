from django import template


register = template.Library()


@register.filter
def process_ingredients(ingredients):
    return ingredients.split(', ')