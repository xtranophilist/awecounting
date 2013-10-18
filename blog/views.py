from django.shortcuts import render, get_object_or_404
from blog.models import Blog


def list_blog_entries(request):
    objs = Blog.objects.all()
    return render(request, 'list_blog_entries.html', {'objs': objs})


def view_blog_entry(request, id):
    obj = get_object_or_404(Blog, id=id)
    return render(request, 'view_blog_entry.html', {'obj': obj})