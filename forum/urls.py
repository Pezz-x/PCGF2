from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.forum_view, name='forum'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('summernote/', include('django_summernote.urls')),
]
