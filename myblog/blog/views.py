from django.shortcuts import render,redirect
from blog.models import Post,UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
	context_data = dict()
	context_data['posts'] = Post.objects.all()
	if request.user.is_authenticated:
		context_data['users'] = UserProfile.objects.all()[:10]
	return render(request, 'home.html', context_data)


def post_details(request, pk):
	context_data = dict()
	try:
		post = Post.objects.get(pk=pk)
	except Post.DoesNotExist:
		post = None

	if post is None:
		context_data['invalid_request'] = True
		return render(request, 'post_details.html', context_data)
	post.views += 1
	post.save()
	context_data['post'] = post
	return render(request, 'post_details.html', context_data)


@login_required(login_url='/user_login/')
def create_post(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		text = request.POST.get('text')
		new_post = Post.objects.create(
			title=title,
			text=text,
			user=request.user,
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
		new_user_profile = UserProfile.objects.create(
			user=new_user
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

@login_required
def user_dashboard(request):
	context_data = dict()
	context_data['user_posts'] = Post.objects.filter(user=request.user).order_by('-created_at')
	return render(request, 'user_dashboard.html', context_data)


@login_required
def user_profile(request):
	if request.method == 'POST':
		user_profile = UserProfile.objects.get(user=request.user)
		user_profile.first_name = request.POST.get('first_name')
		user_profile.last_name = request.POST.get('last_name')
		user_profile.contact_phone = request.POST.get('contact_phone')
		user_profile.profile_pic = request.POST.get('profile_pic')
		user_profile.about = request.POST.get('about')
		user_profile.save()
		return redirect('user_dashboard')
	return render(request, 'user_profile.html')