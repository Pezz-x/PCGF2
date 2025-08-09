from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Allows template usage: {{ my_dict|get_item:some_key }}
    """
    try:
        return dictionary.get(key)
    except AttributeError:
        return None
