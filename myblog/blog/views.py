from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session

from django.contrib.auth.decorators import login_required
from django.db.models import Q

from blog.models import Post,UserProfile,PostLike,PostComment,PostShare,Friendship

# @csrf_exempt
# def node_server_api(request):
# 	try:
# 		session = Session.objects.get(
# 			session_key=request.POST.get('sessionid')
# 		)
# 		user_id = session.get_decoded().get('_auth_user_id')
# 		user = User.objects.get(id=user_id)

# 		# creating comment

def home(request):
	data = request.GET.get('search_item')
	print(data)
	context_data = dict()
	if request.user.is_authenticated:
		if data is None:
			context_data['posts'] = Post.objects.all()
		else:
			context_data['posts'] = Post.objects.filter(
				Q(text__icontains=data) | Q(title__icontains=data)
			)
			context_data['search_posts'] = True
		# request_users = Friendship.objects.filter(request_from=request.user)
		# context_data['users'] = UserProfile.objects.exclude(user=request.user, user__request_from=request.user)[:10]
	return render(request, 'home.html', context_data)


@login_required
def send_friend_request(request, pk):
	request_to_user_profile = UserProfile.objects.get(pk=pk)
	request_to_user = request_to_user_profile.user
	new_friendship = Friendship.objects.create(
		request_from=request.user,
		request_to=request_to_user
	)
	return redirect('home')



@login_required
def accept_friend_request(request,pk):
	frienship_request = Friendship.objects.get(pk=pk)
	frienship_request.is_accepted = True
	frienship_request.save()
	return redirect('home')


@login_required
def reject_friend_request(request, pk):
	frienship_request = Friendship.objects.get(pk=pk)
	frienship_request.delete()
	return redirect('home')


@login_required
def block_friend_request(request, pk):
	frienship_request = Friendship.objects.get(pk=pk)
	frienship_request.is_blocked = True
	frienship_request.save()
	return redirect('home')


@csrf_exempt
@login_required
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
	check_like = PostLike.objects.filter(user=request.user, post=post).exists()
	if check_like:
		context_data['post_liked'] = True

	if request.method == 'POST':
		# try:
		# 	session = Session.objects.get(
		# 		session_key=request.POST.get('sessionid')
		# 	)
		# 	user_id = Session.get_decoded().get('_auth_user_id')
		# 	user = User.objects.get(id=user_id)
		# 	PostComment.objects.create(
		# 		post=post,
		# 		user=user,
		# 		comment=request.POST.get('comment')
		# 	)
		# 	r = redis.StrictRedis(host='localhost', port=6379, db=0)
		# 	r.publish('comment', user=user.username+':'+request.POST.get('comment'))
		# 	return HttpResponse("Ok")
		# except Exception, e:
		# 	return HttpResponseServerError(str(e))
		comment_text = request.POST.get('comment_text')
		comment = PostComment.objects.create(
			post=post,
			user=request.user,
			comment_text=comment_text
		)
		return redirect('post_details', pk=post.id)		
	return render(request, 'post_details.html', context_data)


@login_required
def post_like(request, pk):
	context_data = dict()
	try:
		post = Post.objects.get(pk=pk)
	except Post.DoesNotExist:
		post = None

	new_like = PostLike.objects.create(
		user=request.user,
		post=post
	)
	return redirect('post_details', pk=post.id)


@login_required
def post_dislike(request, pk):
	context_data = dict()
	try:
		post = Post.objects.get(pk=pk)
	except Post.DoesNotExist:
		post = None

	post_like = PostLike.objects.get(user=request.user, post=post)
	post_like.delete()
	return redirect('post_details', pk=post.id)



@login_required
def post_share(request, pk):
	context_data = dict()
	try:
		post = Post.objects.get(pk=pk)
	except Post.DoesNotExist:
		post = None

	post_share = PostShare.objects.create(
		post=post,
		user=request.user
	)
	return redirect('post_details', pk=post.id)


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