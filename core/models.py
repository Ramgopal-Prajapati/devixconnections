from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_id = models.CharField(max_length=50, unique=True)
    nickname = models.CharField(max_length=60, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.student_id})"

    def get_display_name(self):
        return self.nickname if self.nickname else (self.user.get_full_name() or self.user.username)

    def follower_count(self):
        return self.followers.count()

    def following_count(self):
        return Profile.objects.filter(followers=self.user).count()


class Post(models.Model):
    POST_TYPES = [
        ('thought', '💭 Thought'),
        ('study', '📚 Study'),
        ('coaching', '🏫 Coaching'),
        ('about', '👤 About Me'),
        ('photo', '📷 Photo'),
        ('video', '🎥 Video'),
        ('audio', '🎵 Audio'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='thought')
    content = models.TextField(blank=True)
    media = models.FileField(upload_to='posts/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} - {self.post_type} - {self.created_at.strftime('%d %b %Y')}"

    def like_count(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username} on Post #{self.post.id}"
