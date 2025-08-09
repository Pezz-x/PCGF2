from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'images']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'images']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }
