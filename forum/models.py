from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body = models.TextField()
    images = CloudinaryField('images', blank=True, null=True)
    time_created = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    class Meta:
        ordering = ["-time_created"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} | written by {self.author}"
    
    @property
    def likes_count(self):
        return self.liked_by.count()

    @property
    def comments_count(self):
        return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    images = CloudinaryField('images', blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(User, related_name="liked_comments", blank=True)

    class Meta:
        ordering = ["-created_on"]
        
    def __str__(self):
        return f"Comment {self.body}. by {self.author}"
    
    @property
    def likes_count(self):
        return self.liked_by.count()
