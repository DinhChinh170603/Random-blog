from django import forms

from .models import Comment, Post, Category

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'status', 'title', 'intro', 'body', 'image')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)