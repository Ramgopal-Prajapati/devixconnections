from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('feed/', views.feed, name='feed'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('students/', views.students_list, name='students'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('chat/<str:username>/', views.chat_view, name='chat'),
]
