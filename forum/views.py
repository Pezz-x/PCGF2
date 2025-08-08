from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post

# Create your views here.
def forum_view(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('forum')
    else:
        form = PostForm()
    return render(request, 'forum/forum.html', {'posts': posts, 'form': form})
    
def post_detail(request, slug):
    # Replace 'Post' with your actual model name
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'forum/post_detail.html', {'post': post})
