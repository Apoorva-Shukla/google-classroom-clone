from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.core.paginator import Paginator
from django.core.serializers import serialize
from .models import Classroom, Post, Comment
from user.models import Profile
from .forms import PostForm
from classroom.views import basic_vars
import math

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
    form = PostForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == 'POST':
        if request.is_ajax():
            if request.POST.get('_name', '') == 'post':
                if form.is_valid():
                    if not(request.user not in Classroom.objects.filter(slug=slug).first().teachers.all() and request.user not in Classroom.objects.filter(slug=slug).first().students.all()):
                        form.save()
                        return JsonResponse(data={
                            '': '',
                        })

            elif request.POST.get('_name', '') == 'comment':
                comment = Comment(user=request.user, post=Post.objects.filter(pk=int(request.POST.get('post', ''))).first(), text=request.POST.get('text', ''))
                comment.save()

                return JsonResponse(data={
                    'comment': serialize('json', [comment]),
                    'user': f'{request.user.first_name} {request.user.last_name}',
                    'avatar': Profile.objects.filter(user=request.user).first().avatar.url,
                })

    posts = list(Post.objects.filter(classroom=Classroom.objects.filter(slug=slug).first()))[::-1]
    LIMIT = 10
    try:
        PAGE = abs(int(request.GET.get('p', '')))
    except:
        PAGE = 1

    posts = Paginator(posts, LIMIT)
    total_pages = posts.num_pages

    try:
        posts = posts.page(PAGE)
    except:
        posts = []

    return page(request, slug, '_class/stream.html', {
        'posts': posts,
        'form': form,
        'page': PAGE,
        'total_pages': total_pages,
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