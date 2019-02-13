from django.shortcuts import render
from django.utils import timezone
from . models import Post


# Create your views here.
def post_list(request):

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # we till it to render the request... that request object is passed in the post_list.html
    # we render the post_list.html from the template folder in the blog app

    stuff_for_frontend = {'posts': posts}

    return render(request, "blog/post_list.html", stuff_for_frontend)
