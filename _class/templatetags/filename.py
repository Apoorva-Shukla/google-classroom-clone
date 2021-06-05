import os

from django import template


register = template.Library()

@register.filter(name='filename')
def filename(value):
    return os.path.basename(value.file.name)