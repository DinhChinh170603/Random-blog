from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('create/', views.createPost, name='create_post'),
    path('delete/<int:id>', views.delete_post, name='delete_post'),
    path('<slug:category_slug>/<slug:slug>/', views.detail, name = 'post_detail'),
    path('<slug:slug>/', views.category, name = 'category_detail'),
] 