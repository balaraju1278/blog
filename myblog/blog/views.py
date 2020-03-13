from django.shortcuts import render,redirect
from blog.models import Post


def home(request):
	context_data = dict()
	context_data['posts'] = Post.objects.all()
	return render(request, 'home.html', context_data)


def create_post(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		text = request.POST.get('text')
		new_post = Post.objects.create(
			title=title,
			text=text,
		)
		return redirect('home')
	return render(request, 'create_post.html')