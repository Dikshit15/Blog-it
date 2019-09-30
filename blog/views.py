from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.http import HttpResponseRedirect,HttpResponse
from .models import Post,Comment
from django import forms
from .forms import PostForm,CommentForm,SignUpForm
from django.shortcuts import redirect,render_to_response,render
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage,send_mail


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
    #if(post.author!=request.user):
    #    return redirect('post_list',request)
    if request.method=="POST" and post.author==request.user:
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
    if(post.author==request.user):
        post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def post_remove(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if(post.author==request.user):
        post.delete() #Every django model can be deleted by .delete().
    return redirect('post_list')

def signup(request):
    if request.user.is_authenticated:
        #print('Please logout before signing in.')
        return redirect('post_list')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('blog/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})
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
    #return redirect('e')
    return redirect('signup')
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

def account_activation_sent(request):
    return render(request, 'blog/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'blog/account_activation_invalid.html')

def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Your password was successfully updated!')
            send_mail(
            'Password Change Request Status','Your request for password updation has been succesfully executed. Your password is succesfully changed.',
            'dikshitmaheshwari15@gmail.com',['16ucc030@lnmiit.ac.in'],
            )
            #email.send()
            return redirect('change_password')
        else:
            messages.error(request,'Please correct the error below.',extra_tags='alert')
    else:
        form=PasswordChangeForm(request.user)
    return render(request,'blog/change_password.html',{
        'form':form
    })
