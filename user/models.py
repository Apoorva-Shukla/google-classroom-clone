from django.db import models
from django.contrib.auth.models import User
from . import utils

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(default='defaults/user/default_user_img.png', upload_to=utils.avatar_upload)

	def __str__(self):
		return str(self.user.username)