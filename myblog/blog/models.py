from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
	title = models.CharField(max_length=250)
	text = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts', null=True,blank=True)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title