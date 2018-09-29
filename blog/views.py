from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from .models import Post,Comment
from django import forms
from .forms import PostForm,CommentForm
from django.shortcuts import redirect,render_to_response
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
#from .forms import UserRegistrationForm
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

@login_required
def post_new(request):
    if request.method == "POST":
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            #post.published_date=timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=PostForm()
    return render(request,'blog/post_edit.html',{'form':form})

@login_required
def post_edit(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=="POST":
        form=PostForm(request.POST,instance=post)
        if form.is_valid:
            post=form.save(commit=False)
            post.author=request.user
            #post.published_date=timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=PostForm(instance=post)
    return render(request,'blog/post_edit.html',{'form':form})

@login_required
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request,'blog/post_draft_list.html',{'posts':posts})

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def post_remove(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.delete() #Every django model can be deleted by .delete().
    return redirect('post_list')

"""def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj=form.cleaned_data
            username=userObj['username']
            email=userObj['email']
            password=userObj['password']
            if not(User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username,email,password)
                user=authenticate(username=username,password=password)
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        UserRegistrationForm()

    return render(request,'blog/register.html',{'form':form})"""

def signup(request):
    if request.user.is_authenticated:
        #print('Please logout before signing in.')
        return redirect('post_list')
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('Username')
            t_password=form.cleaned_data.get('Password')
            user=form.save()
            login(request,user)
            return redirect('/')
    else:
        form=UserCreationForm()
    return render(request,'blog/signup.html',{'form':form})

def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=CommentForm()
    return render(request,'blog/add_comment_to_post.html',{'form':form})
@login_required
def logout_view(request):
    #if request.method=='POST':
    #    form=UserCreationForm(request.POST)
    #    if form.is_valid():
    #        form.save()
    #        return redirect('/')
    #return render(request,'blog/userlogout.html',{'form':form})
    logout(request)
    #return render_to_response('/^accounts/login/$',message='Goodbye. Looking forward to seeing you at PotterMania.')
    messages.success(request,'Goodbye. Looking forward to seeing you at PotterMania.',extra_tags='alert')
    return redirect('signup')
    #    return redirect('signup')
    #print(logout(request))

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
