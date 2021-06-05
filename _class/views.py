from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from .models import Classroom, Post
from classroom.views import basic_vars

# Create your views here.
def page(request, slug, template, context_data={}):
    user, classes = basic_vars(request)

    class_room = get_object_or_404(Classroom, slug=slug)
    if user not in class_room.teachers.all() and user not in class_room.students.all():
        raise Http404()

    context = {
        'user': user,
        'classes': classes,
        'class': class_room,
    }
    context = dict(list(context.items()) + list(context_data.items()))
    return render(request, f'{template}', context)

def stream_page(request, slug):
    posts = Post.objects.filter(classroom=Classroom.objects.filter(slug=slug).first())
    return page(request, slug, '_class/stream.html', {
        'posts': posts,
    })

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