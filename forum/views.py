from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Post

# Create your views here.
def forum_view(request):
    posts = (
        Post.objects
        .select_related("author")  # assuming author is Profile
        .annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count("comments", distinct=True),
        )
        .order_by("-time_created")  # newest first
    )
    return render(request, "forum/forum.html", {"posts": posts})
    
def post_detail(request, slug):
    # Replace 'Post' with your actual model name
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'forum/post_detail.html', {'post': post})
