import os

from django import template


register = template.Library()

@register.filter(name='file_preview')
def file_preview(value):
    src = 'https://www.vhv.rs/dpng/d/443-4430861_django-python-logo-png-png-download-django-python.png'

    

    return f'<img\
        class="border-end"\
        style="width: 100px; height: auto"\
        src="{src}"\
        alt=" "\
    />'