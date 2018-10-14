from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib import admin

#from .views import register

urlpatterns = [
    #url(r'^$',home),
    #url(r'^register/',register),
    #path('post/register',views.register,name='register.html'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('signup/',views.signup,name='signup'),
    path('logout/', views.logout_view, name='logout_view'),
    path('',views.post_list,name='post_list'),
    path(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    path(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    path(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    path('post/<int:pk>/',views.post_detail,name='post_detail'),
    path('post/new',views.post_new,name='post_new'),
    path('post/<int:pk>/edit/',views.post_edit,name='post_edit'),
    path(r'^drafts/$',views.post_draft_list,name='post_draft_list'),
    path(r'^post/(?P<pk>\d+)/Publish/$', views.post_publish, name='post_publish'),
    path(r'^post/(?P<pk>\d+)/Remove/$', views.post_remove, name='post_remove'),
]
