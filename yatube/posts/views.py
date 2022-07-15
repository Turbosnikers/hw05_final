from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .models import Follow, Group, Post, User
from .forms import CommentForm, PostForm

POSTS_COUNT = 10


def get_page_context(request, queryset):
    paginator = Paginator(queryset, POSTS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
    }


@cache_page(20 * 15)
def index(request):
    context = get_page_context(request, Post.objects.all())
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    context = {
        'group': group,
    }
    context.update(get_page_context(request, group.posts.all()))
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = (
        request.user.is_authenticated
        and author.following.filter(user=request.user).exists()
    )
    context = {
        'author': author,
        'following': following,
    }
    context.update(get_page_context(request, author.posts.all()))
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, id=post_id)
    author_posts_count = post.author.posts.count()
    context = {
        'post': post,
        'form': form,
        'author_posts_count': author_posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@cache_page(20 * 15)
@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', post.author.username)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    context = get_page_context(
        request,
        Post.objects.filter(author__following__user=request.user).all()
    )
    return render(request, 'posts/index.html', context)


@login_required
def profile_follow(request, username):
    following = get_object_or_404(User, username=username)
    if following != request.user:
        Follow.objects.get_or_create(user=request.user, author=following)
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    following = get_object_or_404(User, username=username)
    follower = get_object_or_404(Follow, author=following, user=request.user)
    follower.delete()
    return redirect('posts:profile', username)
