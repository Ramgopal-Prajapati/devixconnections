from django import forms
from .models import Profile, Post, Comment

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'bio', 'avatar']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your nickname...'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Tell something about yourself...'}),
            'avatar': forms.FileInput(attrs={'class': 'file-input', 'accept': 'image/*'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'content', 'media']
        widgets = {
            'post_type': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Share your thoughts...'}),
            'media': forms.FileInput(attrs={'class': 'file-input', 'accept': 'image/*,video/*,audio/*'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'comment-input', 'placeholder': 'Write a comment...'}),
        }
