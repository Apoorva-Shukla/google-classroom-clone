from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Classroom
from classroom.views import basic_vars

# Create your views here.
def page(request, slug, template, context_data={}):
    user, classes = basic_vars(request)

    class_room = Classroom.objects.filter(slug=slug).first()

    context = {
        'user': user,
        'classes': classes,
        'class': class_room,
    }
    context = dict(list(context.items()) + list(context_data.items()))
    return render(request, f'{template}', context)

def stream_page(request, slug):
    return page(request, slug, '_class/stream.html')

def classwork_page(request, slug):
    return page(request, slug, '_class/classwork.html')

def people_page(request, slug):
    class_room = Classroom.objects.filter(slug=slug).first()
    teachers = class_room.teachers.all()
    students = class_room.students.all()

    return page(request, slug, '_class/people.html', {
        'teachers': teachers,
        'students': students,
    })