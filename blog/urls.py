"""cotrearh_blog_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.post_list, name='post_list'),
    re_path(r'logout', views.logout_user, name='logout'),
    re_path(r'login_page', views.login_page, name='login_page'),
    re_path(r'login', views.login_user, name='login'),
    re_path(r'registration', views.registration_page, name='registration'),
    re_path(r'register', views.register, name='register'),
    re_path(r'topics_list$', views.topics_list, name='topics_list'),
    re_path(r'add_topic', views.add_topic, name='add_topic'),
    re_path(r'topics_list/(?P<pk>\d+)/edit/', views.topic_edit, name='topic_edit'),
    re_path(r'topics_list/(?P<pk>\d+)/delete/', views.topic_delete, name='topic_delete'),
    re_path(r'add_post', views.add_post, name='add_post'),
    re_path(r'post_list/(?P<pk>\d+)/edit/', views.edit_post, name='edit_post'),
    re_path(r'post_list/(?P<pk>\d+)/delete/', views.delete_post, name='delete_post'),
    re_path(r'post_list/(?P<pk>\d+)/read/', views.read_post, name='read_post'),
]
