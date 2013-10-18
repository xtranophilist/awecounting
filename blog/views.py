from django.shortcuts import render, get_object_or_404
from blog.models import Blog

try:
    from django.contrib.auth import get_user_model

    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


def list_blog_entries(request):
    objs = Blog.objects.all()
    return render(request, 'list_blog_entries.html', {'objs': objs})


def view_blog_entry(request, id):
    obj = get_object_or_404(Blog, id=id)
    return render(request, 'view_blog_entry.html', {'obj': obj})


def view_blogs_by_author(request, username):
    user = User.objects.get(username=username)
    objs = Blog.objects.filter(author=user)
    return render(request, 'view_blogs_by_author.html', {'objs': objs, 'user': user })