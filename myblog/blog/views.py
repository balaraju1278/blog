from django.shortcuts import render,redirect
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
	context_data = dict()
	context_data['posts'] = Post.objects.all()
	return render(request, 'home.html', context_data)


@login_required(login_url='/user_login/')
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


# user views
def user_registration(request):
	context_data = dict()
	if request.method == 'POST':
		username = request.POST.get('username')
		check_username = User.objects.filter(username=username).exists()
		if check_username:
			context_data['invalid_username'] = True
			return render(request, 'user_registration.html', context_data)
		email = request.POST.get('email')
		check_email = User.objects.filter(email=email).exists()
		if check_email:
			context_data['invalid_email'] = True
			return render(request, 'user_registration.html', context_data)

		new_user = User.objects.create(
			username=username,
			email=email
		)
		new_user.set_password(request.POST.get('password'))
		new_user.save()
		return redirect('user_login')
	return render(request, 'user_registration.html', context_data)


def user_login(request):
	context_data = dict()
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		try:
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('home')
		except:
			context_data['invalid_data'] = True
			return render(request, 'user_login.html', context_data)
	return render(request, 'user_login.html')


def user_logout(request):
	logout(request)
	return redirect('user_login')