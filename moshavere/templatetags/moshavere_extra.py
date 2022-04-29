from django import template

register = template.Library()

@register.filter(name='split_ret_last')
def split_ret_last(value, arg):
    result = value.split(arg)[-1]
    return result