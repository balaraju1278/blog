from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
	title = models.CharField(max_length=250)
	text = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts', null=True,blank=True)
	views = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.title


class PostLike(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')

	def __str__(self):
		return '{}---{}'.format(str(self.post),str(self.user))	


class PostComment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commented_posts')
	comment_text = models.TextField()
	commented_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.comment_text


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
	first_name = models.CharField(max_length=100,null=True,blank=True)
	last_name = models.CharField(max_length=100, null=True, blank=True)
	contact_phone = models.CharField(max_length=12, null=True,blank=True)
	profile_pic = models.ImageField(upload_to='images/', null=True,blank=True)
	about = models.TextField(null=True,blank=True)

	def __str__(self):
		return str(self.user)