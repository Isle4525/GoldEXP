from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
from posts.models import Post


def comment_list(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    return render(request, 'comments/list.html', {'post': post, 'comments': comments})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('comments:comment_list', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'comments/add.html', {'form': form, 'post': post})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        return redirect('comments:comment_list', post_id=comment.post.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('comments:comment_list', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'comments/edit.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    if comment.author == request.user:
        comment.delete()
    return redirect('comments:comment_list', post_id=post_id)


@login_required
def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, pk=comment_id)
    post = parent_comment.post

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.post = post
            reply.parent = parent_comment
            reply.save()
            return redirect('comments:comment_list', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'comments/reply.html', {'form': form, 'parent': parent_comment})
