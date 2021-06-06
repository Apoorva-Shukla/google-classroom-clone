from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from .models import Classroom, Post
from .forms import PostForm
from classroom.views import basic_vars
from django.core.serializers import serialize
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
            if form.is_valid():
                if not(request.user not in Classroom.objects.filter(slug=slug).first().teachers.all() and request.user not in Classroom.objects.filter(slug=slug).first().students.all()):
                    form.save()

                    cr = Classroom.objects.filter(slug=slug).first()
                    this_post = Post.objects.filter(classroom=cr, user=request.user).last()
                    this_post = serialize('json', [this_post])

                    return JsonResponse(data={
                        'this_post': this_post,
                    })

    posts = Post.objects.filter(classroom=Classroom.objects.filter(slug=slug).first())
    total_querysets = posts.count()
    posts = list(posts)[::-1]


    LIMIT = 10
    try:
        PAGE = int(request.GET.get('p', ''))
    except:
        PAGE = 1
    number_of_pages = int(math.ceil(total_querysets / LIMIT))

    start = (PAGE - 1) * LIMIT
    end = start + LIMIT
    return page(request, slug, '_class/stream.html', {
        'posts': posts[start:end],
        'form': form,
        'page': PAGE,
        'total_pages': number_of_pages,
        'limit': LIMIT,
        'pagi_range': range(PAGE, PAGE+3),
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