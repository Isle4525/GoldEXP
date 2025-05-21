from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Tag, PostRating
from .forms import PostForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.http import urlencode
from django.db.models import Avg
from comments.models import Comment
from comments.forms import CommentForm



def home(request):
    return render(request, 'base.html')


def post_list(request):
    posts = Post.objects.filter(is_published=True)
    category = request.GET.get('category')
    tag = request.GET.get('tag')
    search = request.GET.get('search')

    if category:
        posts = posts.filter(category=category)
    if tag:
        posts = posts.filter(tags__name=tag)
    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(tags__name__icontains=search)
        ).distinct()

    paginator = Paginator(posts, 5)  # 5 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
        'categories': dict(Post.CATEGORIES),
    }
    return render(request, 'posts/list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()

    comments = Comment.objects.filter(post=post, parent=None).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'posts/detail.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # for tags
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})

@login_required
def rate_post(request, pk, value):
    post = get_object_or_404(Post, pk=pk)
    rating, created = PostRating.objects.get_or_create(
        post=post, 
        user=request.user,
        defaults={'value': value}
    )
    if not created:
        if rating.value == value:
            rating.delete()
        else:
            rating.value = value
            rating.save()
    return redirect('post_detail', pk=post.pk)