from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .forms import CommentForm, PostForm
from .models import Category, Post

# Create your views here.
def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect('post_detail', category_slug = category_slug, slug=slug)
    else:
        form = CommentForm()

    form = CommentForm()

    return render(request, 'blog/detail.html', {'post': post, 'form': form})

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)
    
    return render(request, 'blog/category.html', {'category': category, 'posts': posts})


def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

    return render(request, 'blog/search2.html', {'posts': posts, 'query': query})

def createPost(request):
    if (request.method == 'POST'):
        form = PostForm(request.POST)
        if (form.is_valid()):
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.author = request.user
            post.save()
            return redirect('frontpage')

    form = PostForm()

    return render(request, 'blog/create_post.html', {'post_form': form})
        
