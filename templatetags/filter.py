from django import template

register = template.Library()


@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='split')
def split(value, key):
    return value.split(key)[0]
