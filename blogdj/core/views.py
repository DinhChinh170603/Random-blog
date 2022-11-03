from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from .forms import NewUserForm

from blog.models import Post

# Create your views here.


def frontpage(request):
    posts = Post.objects.filter(status=Post.ACTIVE)
    return render(request, 'core/frontpage.html', {'posts': posts})


def about(request):
    return render(request, 'core/about.html')


def robots_txt(request):
    text = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(text), content_type="text/plain")


def register(request):
    if request.method == 'POST':
        register_form = NewUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            auth_login(request, user)
            messages.success(request, "Registered successfully!")
            return redirect('frontpage')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    register_form = NewUserForm()
    return render(request, 'core/register.html', {'register_form': register_form})


def login(request):
    if request.user.is_authenticated:
        return redirect('frontpage')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("frontpage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="core/login.html", context={"login_form": form})
