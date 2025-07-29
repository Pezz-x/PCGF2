from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    # images = TODO
    time_created = models.DateTimeField(auto_now=True)
    # likes = models.Count() TO RESEARCH

    class Meta:
        ordering = ["-time_created"]

    def __self__(self):
        return f"{self.title}| wiritten by {self.author}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    # images = TODO
    created_on = models.DateTimeField(auto_now=True)
    # likes = models.Count() TO RESEARCH

    class Meta:
        ordering = ["-created_on"]
        
    def __str__(self):
        return f"Comment {self.body}. by {self.author}"
