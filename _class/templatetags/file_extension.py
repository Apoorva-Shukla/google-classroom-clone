import os

from django import template


register = template.Library()

@register.filter(name='file_extension')
def file_extension(value):
    return os.path.basename(value.file.name).split('.')[-1].upper()