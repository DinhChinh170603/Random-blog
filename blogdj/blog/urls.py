from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('profile/<str:author>', views.profile, name='profile'),
    path('create_post/', views.createPost, name='create_post'),
    path('create_category', views.createCategory, name='create_category'),
    path('set_active/<int:id>', views.set_active, name='set_active'),
    path('set_draft/<int:id>', views.set_draft, name='set_draft'),
    path('delete_post/<int:id>', views.delete_post, name='delete_post'),
    path('delete_comment/<int:post_id>/<int:id>', views.delete_comment, name='delete_comment'),
    path('<slug:category_slug>/<slug:slug>/<int:id>', views.detail, name = 'post_detail'),
    path('<slug:slug>/', views.category, name = 'category_detail'),
] 