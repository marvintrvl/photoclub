from django import template
from members.models import Equipment

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_display_category(value):
    return dict(Equipment.CATEGORIES).get(value, value)