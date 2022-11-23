from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('create_post/', views.createPost, name='create_post'),
    path('create_category', views.createCategory, name='create_category'),
    path('delete_post/<int:id>', views.delete_post, name='delete_post'),
    path('<slug:category_slug>/<slug:slug>/delete_comment/<int:id>', views.delete_comment, name='delete_comment'),
    path('<slug:category_slug>/<slug:slug>/<int:id>', views.detail, name = 'post_detail'),
    path('<slug:slug>/', views.category, name = 'category_detail'),
] 