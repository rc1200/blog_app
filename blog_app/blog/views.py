from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.utils import timezone

from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # we till it to render the request... that request object is passed in the post_list.html
    # we render the post_list.html from the template folder in the blog app

    stuff_for_frontend = {'posts': posts}
    return render(request, "blog/post_list.html", stuff_for_frontend)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if str(request.user) != 'AnonymousUser':
        permissions = Permission.objects.filter(user=request.user)
        # print(permissions)
        # for a in permissions:
        #     print(a)
        comments_filtered = Comment.objects.filter(post_id=pk)
    else:
        comments_filtered = Comment.objects.filter(approved=True, post_id=pk)
        post = Post.objects.filter(published_date__isnull=False)


    # Permissions that the user has via a group
    # group_permissions = Permission.objects.filter(group__user=request.user)

    stuff_for_frontend = {'post': post, 'comments_filtered': comments_filtered}
    return render(request, 'blog/post_detail.html', stuff_for_frontend)

@login_required
def post_new(request):
    template_name = 'new'
    if request.method == 'POST':
        form = PostForm(request.POST)  # if post then capture all that data and store it in an object
        if form.is_valid():  # ensure the form has clean data passed
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            # return redirect('post_detail', pk=post.pk)
            return redirect('post_detail', pk=post.pk)
    else:
        # just renders the form, so when you submit the data is there since you filled it out
        form = PostForm()
        stuff_for_frontend = {'form': form}

    return render(request, 'blog/post_edit.html', stuff_for_frontend)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # update existing form
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.authoer = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        stuff_for_frontend = {'form': form}
    return render(request, 'blog/post_edit.html', stuff_for_frontend)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("post_list")


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    stuff_for_frontend = {'posts': posts}
    return render(request, "blog/post_draft_list.html", stuff_for_frontend)

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published_date = timezone.now()
    post.save()

    stuff_for_frontend = {'post': post}
    return render(request, 'blog/post_detail.html', stuff_for_frontend)

@login_required
def post_unPublish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.published_date = None
    post.save()

    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    stuff_for_frontend = {'posts': posts}
    return render(request, "blog/post_draft_list.html", stuff_for_frontend)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST' and 'save_btn' in request.POST:
        # update existing form
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    elif request.method == 'POST' and 'cancel_btn' in request.POST:
        return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form' : form })

@login_required
def comment_edit(request, pk):
    post = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST' and 'save_btn' in request.POST:
        form = CommentForm(request.POST, instance=post)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return redirect('post_detail', pk=comment.post_id)
    elif request.method == 'POST' and 'delete_btn' in request.POST:
        post.delete()
        return redirect('post_detail', pk=post.post_id)
    else:
        form = CommentForm(instance=post)

    return render(request, 'blog/comment_edit.html', {'form' : form })


@login_required
def comment_publish(request, pk):
    post = get_object_or_404(Comment, pk=pk)

    if post.approved:
        post.un_approve_post()
    else:
        post.approve_post()

    return redirect('post_detail', pk=post.post.id)

