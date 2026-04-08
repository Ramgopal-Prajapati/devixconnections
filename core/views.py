from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Profile, Post, Comment
from .forms import ProfileEditForm, PostForm, CommentForm
from django.db.models import Q

def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('feed')
        else:
            messages.error(request, 'Invalid Student ID or Password.')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def feed(request):
    posts = Post.objects.select_related('author', 'author__profile').prefetch_related('likes', 'comments').all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post shared!')
            return redirect('feed')
    return render(request, 'core/feed.html', {'posts': posts, 'form': form})

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)
    posts = Post.objects.filter(author=profile_user)
    is_following = profile.followers.filter(id=request.user.id).exists()
    return render(request, 'core/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
    })

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def students_list(request):
    profiles = Profile.objects.select_related('user').all()
    q = request.GET.get('q', '')
    if q:
        profiles = profiles.filter(
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q) |
            Q(student_id__icontains=q) |
            Q(nickname__icontains=q)
        )
    return render(request, 'core/students.html', {'profiles': profiles, 'q': q})

@login_required
@require_POST
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=target_user)
    if target_user == request.user:
        return JsonResponse({'error': 'Cannot follow yourself'}, status=400)
    if profile.followers.filter(id=request.user.id).exists():
        profile.followers.remove(request.user)
        following = False
    else:
        profile.followers.add(request.user)
        following = True
    return JsonResponse({'following': following, 'count': profile.follower_count()})

@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': post.like_count()})

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        profile = getattr(request.user, 'profile', None)
        avatar_url = profile.avatar.url if profile and profile.avatar else ''
        return JsonResponse({
            'success': True,
            'author': profile.get_display_name() if profile else request.user.username,
            'content': comment.content,
            'avatar': avatar_url,
            'created_at': comment.created_at.strftime('%d %b, %I:%M %p'),
        })
    return JsonResponse({'success': False}, status=400)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user or request.user.is_staff:
        post.delete()
        messages.success(request, 'Post deleted.')
    return redirect('feed')

@login_required
def chat_view(request, username):
    other_user = get_object_or_404(User, username=username)
    return render(request, 'core/chat.html', {'other_user': other_user})
