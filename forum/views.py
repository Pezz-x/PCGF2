from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from .forms import PostForm, CommentForm
from .models import Post, Comment

# Create your views here.

# FOURM PAGE
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
    
# POST DETAIL PAGE
@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()  # related_name in Comment model

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=post.slug)  # Redirect after POST
    else:
        form = CommentForm()

    return render(request, 'forum/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

# POST EDIT PAGE
@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'forum/post_edit.html', {'form': form, 'post': post})

# POST DELETE PAGE
@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        post.delete()
        return redirect('forum')
    return render(request, 'forum/post_confirm_delete.html', {'post': post})

# POST LIKE TOGGLE
@login_required
@require_POST
def post_like_toggle(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user
    if user in post.liked_by.all():
        post.liked_by.remove(user)
        liked = False
    else:
        post.liked_by.add(user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': post.likes_count})

# POST COMMENT PAGE
@login_required
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comment_form': form})

# COMMENT LIKE TOGGLE
@login_required
@require_POST
def comment_like_toggle(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user
    if user in comment.liked_by.all():
        comment.liked_by.remove(user)
        liked = False
    else:
        comment.liked_by.add(user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': comment.likes_count})

# COMMENT EDIT PAGE
@login_required
def comment_edit(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post__slug=slug)
    post = comment.post  # Get related post

    if request.user != comment.author and not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'forum/comment_edit.html', {
        'form': form,
        'comment': comment,
        'post': post
    })

# COMMENT DELETE PAGE
@login_required
def comment_delete(request, slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post__slug=slug)
    post = comment.post

    if request.user != comment.author and not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', slug=slug)

    return render(request, 'forum/comment_confirm_delete.html', {
        'comment': comment,
        'post': post
    })


