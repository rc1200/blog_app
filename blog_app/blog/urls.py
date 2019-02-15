from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 127.0.0.1:8000 so look at the views.post_list view and render that.
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    re_path(r'^post/new/$', views.post_new, name='post_new'),
    # path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('draft_list/', views.post_draft_list, name='post_draft_list'),
    path('draft/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('draft/<int:pk>/unPublish/', views.post_unPublish, name='post_post_unPublish'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'), # look at Templates / registration / login.html
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

]
