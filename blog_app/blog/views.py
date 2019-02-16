from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm, CommentForm
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # we till it to render the request... that request object is passed in the post_list.html
    # we render the post_list.html from the template folder in the blog app

    stuff_for_frontend = {'posts': posts}
    return render(request, "blog/post_list.html", stuff_for_frontend)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    stuff_for_frontend = {'post': post}
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


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # update existing form
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form' : form })
