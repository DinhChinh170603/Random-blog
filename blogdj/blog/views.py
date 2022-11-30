from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .forms import CategoryForm, CommentForm, PostForm
from .models import Category, Post, Comment

# Create your views here.
def detail(request, category_slug, slug, id):
    post = get_object_or_404(Post, slug=slug, id = id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    reply_comment = form.save(commit=False)
                    reply_comment.parent = parent_obj
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect('post_detail', category_slug = category_slug, slug=slug, id=id)
    else:
        form = CommentForm()

    form = CommentForm()

    return render(request, 'blog/detail.html', {'post': post, 'form': form})

def profile(request, author):
    if author == request.user.username:
        posts = Post.objects.filter(author__username=author)
    else:
        posts = Post.objects.filter(author__username=author, status=Post.ACTIVE)

    return render(request, 'blog/profile.html', {'posts': posts, 'username': author})
    
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
        form = PostForm(request.POST, request.FILES)
        if (form.is_valid()):
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            return redirect('post_detail', post.category.slug, post.slug, post.id)

    form = PostForm()

    return render(request, 'blog/create_post.html', {'post_form': form})

def createCategory(request):
    if (request.method == 'POST'):
        form = CategoryForm(request.POST)
        if (form.is_valid()):
            category = form.save(commit=False)
            category.slug = slugify(category.title)
            category.save()
            return redirect('create_post')
        
    form = CategoryForm()

    return render(request, 'blog/create_category.html', {'form': form})
        
def delete_post(request, id):
    post = Post.objects.get(id = id)
    post.delete()
    return redirect('frontpage')

def delete_comment(request, post_id, id):
    comment = Comment.objects.get(id = id)
    post = Post.objects.get(id = post_id)
    comment.delete()
    return redirect('post_detail', category_slug = post.category.slug, slug=post.slug, id=post_id)

def set_active(request, id):
    post = Post.objects.get(id = id)
    post.status = Post.ACTIVE
    post.save()
    return redirect('profile', post.author.username)

def set_draft(request, id):
    post = Post.objects.get(id = id)
    post.status = Post.DRAFT
    post.save()
    return redirect('profile', post.author.username)
