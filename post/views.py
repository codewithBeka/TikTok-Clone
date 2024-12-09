from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from post.models import Stream, Post, Tag,Likes,Follow
from post.forms import NewPostForm,PostUpdateForm
from notifications .models import Notification
from django.contrib.auth.decorators import login_required
from django.template import loader
from authy.models import Profile
from comment.models import Comment,CommentLikes
from comment.forms import CommentForm
from django.contrib.auth.models import User, auth
from django.urls import reverse
from django.db.models import Q
from django.views.generic import ListView
import json
from django.http import JsonResponse

# Create your views here.
from django.db.models import Q

def home(request):
	if request.user.is_authenticated:
		user = request.user
		profile = Profile.objects.get(user=user)

		# Get all the posts
		posts = Post.objects.order_by('-posted')

		# Get all the users the user is not following
		users_not_following = User.objects.exclude(id__in=Follow.objects.filter(follower=user).values_list('following_id', flat=True))[:5]

		context = {
			'posts': posts,
			'all_users': users_not_following,
		}
	else:
		# If the user is not logged in, only display the posts
		posts = Post.objects.order_by('-posted')
		context = {
			'posts': posts,
		}

	return render(request, 'home.html', context)

@login_required
def homeLikes(request):
	user = request.user
	post_id = request.GET.get('post_id')

	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	liked = Likes.objects.filter(post_id=post_id, user=user).count()
	

	if not liked:
				like = Likes.objects.create(user=user, post_id=post_id)
				like.save()
				current_likes = current_likes + 1
				post.likes = current_likes
				post.userlike =True
				post.save()
				return redirect('/')

	else:
			Likes.objects.filter(user=user,post_id=post_id).delete()
			current_likes = current_likes - 1
			post.likes = current_likes
			post.userlike =False
			post.save()
			return redirect('/')
	

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if not Likes.objects.filter(post=post, user=user).exists():
        like = Likes.objects.create(post=post, user=user)
        like.save()
        post.likes += 1
        post.userlike = True
        post.save()

        # Create a notification for the post owner
        notify = Notification.objects.create(
            post=post, sender=user, user=post.user, notification_type=1
        )
        notify.save()

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def unlike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if Likes.objects.filter(post=post, user=user).exists():
        like = Likes.objects.get(post=post, user=user)
        like.delete()
        post.likes -= 1
        post.userlike = False
        post.save()

        # Delete the notification for the post owner
        notify = Notification.objects.filter(
            post=post, sender=user, notification_type=1
        ).first()
        if notify:
            notify.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))




@login_required
def NewPost(request):
	user = request.user
	tags_objs = []

	if request.method == 'POST':
		form = NewPostForm(request.POST, request.FILES)
		if form.is_valid():
			video= form.cleaned_data.get('video')
			caption = form.cleaned_data.get('caption')
			tags_form = form.cleaned_data.get('tags')

			tags_list = list(tags_form.split(','))

			for tag in tags_list:
				t, created = Tag.objects.get_or_create(title=tag)
				tags_objs.append(t)


			# Create the Post object only once
			p, created = Post.objects.get_or_create(video=video, caption=caption, user=user)
			p.tags.set(tags_objs)
			p.save()
			return redirect('home')
	else:
		form = NewPostForm()

	context = {
		'form': form,
		"tags":tags
	}

	return render(request, 'upload.html', context)

@login_required
def update_post(request, post_id):
	user = request.user
	post = get_object_or_404(Post, id=post_id, user=user)

	if request.method == 'POST':
		form = PostUpdateForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.tags.clear()  # Clear existing tags
			# Add new tags
			for tag_name in form.cleaned_data['tags'].split(','):
				tag, _ = Tag.objects.get_or_create(title=tag_name.strip())
				post.tags.add(tag)
			post.save()
			return redirect('home')
	else:
		initial_data = {
			'video': post.video,
			'caption': post.caption,
			'tags': ', '.join(tag.title for tag in post.tags.all()),
		}
		form = PostUpdateForm(instance=post, initial=initial_data)

	context = {
		'form': form,
		'post': post,
	}
	return render(request, 'update.html', context)


# @login_required
# def update_post(request, post_id):
#     user = request.user
#     post = get_object_or_404(Post, id=post_id, user=user)

#     if request.method == 'POST':
#         form = PostUpdateForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = PostUpdateForm(instance=post)

#     context = {
#         'form': form,
#         'post': post,
#     }

#     return render(request, 'update.html', context)


# @login_required
# def update_post(request, post_id):
# 	user = request.user
# 	post = get_object_or_404(Post, id=post_id, user=user)

# 	if request.method == 'POST':
# 		form = PostUpdateForm(request.POST, request.FILES, instance=post, user=user)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('home')
# 	else:
# 		form = PostUpdateForm(instance=post, user=user)

# 	context = {
# 		'form': form,
# 		'post': post,
# 	}

# 	return render(request, 'update.html', context)

@login_required(login_url='login')
def deletePost(request, post_id):
	post = Post.objects.get(id=post_id)

	if request.user != post.user:
		return HttpResponse('Your are not allowed here!!')

	if request.method == 'POST':
		post.delete()
		return redirect('home')
	return render(request, 'delete.html', {'obj': post})



def PostDetails(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	user = request.user
	favorited = False

	#comment
	comments = Comment.objects.filter(post=post).order_by('date')
	
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=user)
		#For the color of the favorite button

		if profile.favorites.filter(id=post_id).exists():
			favorited = True

	#Comments Form
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.user = user
			comment.save()
			return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
	else:
		form = CommentForm()


	template = loader.get_template('postdetail.html')

	context = {
		'post':post,
		'favorited':favorited,
		'form':form,
		'comments':comments,
	}

	return HttpResponse(template.render(context, request))


def tags(request, tag_slug):

	
	tag = get_object_or_404(Tag, slug=tag_slug)
	posts = Post.objects.filter(tags=tag).order_by('-posted')

	template = loader.get_template('tags.html')

	context = {
		'posts':posts,
		'tag':tag,
	}

	return HttpResponse(template.render(context, request))

@login_required
def like(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	liked = Likes.objects.filter(post_id=post_id, user=user).count()

	if not liked:
				like = Likes.objects.create(user=user, post_id=post_id)
				like.save()
				current_likes = current_likes + 1
				post.likes = current_likes
				post.save()

	else:
			Likes.objects.filter(user=user,post_id=post_id).delete()
			current_likes = current_likes - 1
			post.likes = current_likes
			post.save()

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))



@login_required
def favorite(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites.filter(id=post_id).exists():
		profile.favorites.remove(post)
		post.postsaved = False
	else:
		profile.favorites.add(post)
		post.postsaved = True

	profile.save()
	post.save()

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))



@login_required
def savePost(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favorites.filter(id=post_id).exists():
        profile.favorites.remove(post)
        post.postsaved = False
    else:
        profile.favorites.add(post)
        post.postsaved = True

    profile.save()
    post.save()

    return redirect("home")





def search_users(request):
    query = request.GET.get('query')
    if query:
        profiles = Profile.objects.filter(
            Q(user__username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        posts = Post.objects.filter(user__profile__in=profiles).order_by('-posted')
		
    else:
        profiles = None
        posts = None
    context = {
        'profiles': profiles,
        'posts': posts
    }
    return render(request, 'search.html', context)




@login_required
def post_save(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    # Add the post to the user's favorites
    user.profile.favorites.add(post)
    post.saved_by.add(user)
    post.save()  # This will update the num_saves field

    return redirect('home')

@login_required
def post_unsave(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    # Remove the post from the user's favorites
    user.profile.favorites.remove(post)
    post.saved_by.remove(user)
    post.save()  # This will update the num_saves field

    return redirect('home')


def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    # Check if the user has already liked the comment
    try:
        comment_like = CommentLikes.objects.get(user=user, comment=comment)
        comment_like.delete()  # Unlike the comment
        return redirect('post_detail', pk=comment.post.id)
    except CommentLikes.DoesNotExist:
        # Create a new like for the comment
        CommentLikes.objects.create(user=user, comment=comment)
        return redirect('post_detail', pk=comment.post.id)