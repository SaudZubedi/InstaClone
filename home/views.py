from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

from account.models import User
from account.decorators import authorizedUserCanView

from .models import Comment, Follow, Post, PostLike, SavedPost
from .forms import CreatePostForm, CommentForm, EditComment


@authorizedUserCanView
def home_view(request):
    posts = Post.objects.all()
    form = CommentForm()

    users = User.objects.all()[:5]


    context = {
        'posts': posts,
        'form': form,
        'users': users,
    }
    search = request.GET.get('search')

    if search:
        results = User.objects.filter(username__icontains=search)
        context['results'] = results
    else:
        User.objects.all()
        search = ''
    
    return render(request, 'home/home.html', context)


def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)

    user_posts = user.post_set.all()

    all_posts = Post.objects.filter(user=user).count
    following = Follow.objects.filter(user=user).count
    followers = Follow.objects.filter(following=user).count
    try:
        Follow.objects.get(user=request.user, following=user)
        obj = True
    except:
        obj = False

    if request.POST:
        if 'follow' in request.POST:
            try:
                obj = Follow.objects.get(user=request.user, following=user)
                obj.delete()
            except:
                Follow.objects.create(user=request.user, following=user)

    context = {
        'obj': obj,
        'user': user,
        'all_posts': all_posts,
        'following': following,
        'followers': followers,
        'user_posts': user_posts,
    }
    search = request.GET.get('search')
    if search:
        results = User.objects.filter(username__icontains=search)
        context['results'] = results
    else:
        User.objects.all()
        search = ''

    return render(request, 'home/user_profile.html', context)

# CRUD VIEWS 
@authorizedUserCanView
def create_post_view(request):
    form = CreatePostForm()

    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user      #  NOTE: I'm using this method because I actually don't know how do it in any other way. If you have a better way then please kindly let me know.
            obj.save()
            return redirect('home:home')


    context = {'form': form}
    search = request.GET.get('search')
    if search:
        results = User.objects.filter(username__icontains=search)
        context['results'] = results
    else:
        User.objects.all()
        search = ''
    return render(request, 'home/crud/post_form.html', context)

@authorizedUserCanView
def update_post_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user.username != post.user.username:
        print(f'Post: {post.user.username}')
        print(f'Current: {request.user.username}')
        return redirect('home:home')
    elif request.user.username == post.user.username:
        print(f'Post: {post.user.username}')
        print(f'Current: {request.user.username}')
        form = CreatePostForm(instance=post)
        if request.method == 'POST':
            form = CreatePostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post Updated.')
                return redirect('home:home')
            else:
                messages.error(request, 'Could Update your post.')
        
        context = {'form': form}
        search = request.GET.get('search')
        if search:
            results = User.objects.filter(username__icontains=search)
            context['results'] = results
        else:
            User.objects.all()
            search = ''
        return render(request, 'home/crud/post_form.html', context)

@authorizedUserCanView
def delete_post_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user.username != post.user.username:
        print(f'Post: {post.user.username}')
        print(f'Current: {request.user.username}')
        return redirect('home:home')
    elif request.user.username == post.user.username:
        
        if request.method == 'POST':
            post.delete()
            messages.success(request, 'Post Deleted.')
            return redirect('home:home')

        context = {'post': post}
        search = request.GET.get('search')
        if search:
            results = User.objects.filter(username__icontains=search)
            context['results'] = results
        else:
            User.objects.all()
            search = ''
        return render(request, 'home/crud/delete.html', context)

@authorizedUserCanView
def explore_view(request):
    posts = Post.objects.all()

    context = {'posts': posts}
    search = request.GET.get('search')
    if search:
        results = User.objects.filter(username__icontains=search)
        context['results'] = results
    else:
        User.objects.all()
        search = ''
    return render(request, 'home/explore.html', context )


def post_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = CommentForm()

    comments = Comment.objects.filter(post=post)
    likes = PostLike.objects.filter(post=post).count()
    user = request.user

    # To check if the user already likes this post or not,
    # so that I can run a "IF" statement in the HTML document and display the proper icon,
    # to like or to unlike.
    try:
        PostLike.objects.get(user=request.user, post=post)
        print('User already likes this post')
        post_liked = True
    except:
        print('User doesnt likes this post')
        post_liked = False

    # To check if the user has this post saved to not,
    # So I can display the proper icon in the HTML document.
    try:
        SavedPost.objects.get(user=request.user, post=post)
        post_saved = True
    except:
        post_saved = False

    if request.method == 'POST':
        if 'addcomment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.post = post
                obj.user = request.user
                obj.save()

        if 'likebtn' in request.POST:

            try:
                like = PostLike.objects.get(user=user, post=post)
                like.delete()
            except:
                PostLike.objects.create(user=user, post=post)
        
        if 'save' in request.POST:
            try:
                post = SavedPost.objects.get(user=user, post=post)
                post.delete()
            except:
                SavedPost.objects.create(user=user, post=post)
        
        if 'deleteComment' in request.POST:
            id = request.POST.get('comment_id')
            comment = Comment.objects.get(id=id)
            comment.delete()


    context = {
        'post_liked': post_liked,
        'post_saved': post_saved,
        'comments': comments,
        'likes': likes,
        'post': post,
        'form': form,
    }

    search = request.GET.get('search')
    if search:
        results = User.objects.filter(username__icontains=search)
        context['results'] = results
    else:
        User.objects.all()
        search = ''
    return render(request, 'home/post.html', context)


@authorizedUserCanView
def saved_post_view(request):
    all_posts = Post.objects.filter(user=request.user).count
    following = Follow.objects.filter(user=request.user).count
    followers = Follow.objects.filter(following=request.user).count
    
    saved_posts = SavedPost.objects.filter(user=request.user)
    context = {
        'saved_posts': saved_posts,
        'following': following,
        'followers': followers,
        'all_posts': all_posts,
    }
    
    search = request.GET.get('search')
    if search:
        results = User.objects.filter(username__icontains=search)
        context['results'] = results
    else:
        User.objects.all()
        search = ''

    return render(request,'home/saved.html', context)


def features_views(request):
    return render(request, 'home/features.html')