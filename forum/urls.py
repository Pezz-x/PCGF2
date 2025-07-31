from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_view, name='forum'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
