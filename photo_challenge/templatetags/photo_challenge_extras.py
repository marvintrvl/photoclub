from django import template

register = template.Library()

@register.filter
def get_image(submission, image_number):
    return getattr(submission, f'image{image_number}')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)