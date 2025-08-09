from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.forum_view, name='forum'),
    path('forum/<slug:slug>/post_detail/', views.post_detail, name='post_detail'),
    path('forum/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('forum/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('api/post/<slug:slug>/like/', views.post_like_toggle, name='post_like_toggle'),

    path('forum/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('forum/<slug:slug>/comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('forum/<slug:slug>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('api/comment/<int:slug>/like/', views.comment_like_toggle, name='comment_like_toggle'),

    path('summernote/', include('django_summernote.urls')),
]
