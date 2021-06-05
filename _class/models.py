from django.db import models
from django.contrib.auth.models import User
import random, string
from . import utils

# Create your models here.
class Classroom(models.Model):
    # info
    name = models.CharField(max_length=30)
    subject = models.CharField(max_length=50, blank=True)
    standard = models.CharField(max_length=30, blank=True)

    # Unique slug
    slug = models.SlugField(max_length=40, blank=True)

    # members
    teachers = models.ManyToManyField(User, related_name='teachers')
    students = models.ManyToManyField(User, related_name='students')

    # time
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            ran = 'abcd'
            S = random.randint(20, 40)  # number of characters in the string.
            while Classroom.objects.filter(slug=ran).count() != 0 or ran == 'abcd':
                ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
            self.slug = ran
        return super().save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='classroom')

    text = models.TextField(max_length=500, blank=True)
    file = models.FileField(upload_to=utils.file_upload, blank=True)

    # time
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.text