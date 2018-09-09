from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from .models import Post
# git commit -a This is an important command.
def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request,'blog/post_list.html',{'posts': posts})
# This is a sample.
#render function puts together our template blog/post_list.html
#post.objects.get(pk=pk)
def post_detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    return render(request,'blog/post_detail.html',{'post':post})
