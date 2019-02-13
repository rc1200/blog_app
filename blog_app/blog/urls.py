from django.urls import path
from . import views
urlpatterns = [
    # 127.0.0.1:8000 so look at the views.post_list view and render that.
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail')
]