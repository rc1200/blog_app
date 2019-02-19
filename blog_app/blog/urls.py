from django.urls import path, re_path
from . import views

urlpatterns = [
    # 127.0.0.1:8000 so look at the views.post_list view and render that.
    path('post/test/', views.htmltest, name='htmltest'),
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    re_path(r'^post/new/$', views.post_new, name='post_new'),
    # path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('draft_list/', views.post_draft_list, name='post_draft_list'),
    path('draft/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('draft/<int:pk>/unPublish/', views.post_unPublish, name='post_post_unPublish'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/<int:pk>/comment_edit/', views.comment_edit, name='comment_edit'),
    path('post/<int:pk>/comment_publish/', views.comment_publish, name='comment_publish'),
    path('blog/signup/', views.signup, name='signup'),

]
