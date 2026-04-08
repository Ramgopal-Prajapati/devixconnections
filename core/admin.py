from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Post, Comment

admin.site.site_header = "DeviX Connections — Admin Panel"
admin.site.site_title = "DeviX Admin"
admin.site.index_title = "Welcome, Ram Sir 👋"

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 1
    fields = ('student_id', 'nickname', 'bio', 'avatar')

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ('username', 'get_full_name', 'email', 'get_student_id', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'profile__student_id')

    def get_student_id(self, obj):
        try:
            return obj.profile.student_id
        except:
            return '-'
    get_student_id.short_description = 'Student ID'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            pass
        return form

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'nickname', 'follower_count', 'created_at')
    search_fields = ('user__username', 'student_id', 'nickname')
    readonly_fields = ('created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_type', 'content_preview', 'like_count', 'created_at')
    list_filter = ('post_type', 'created_at')
    search_fields = ('author__username', 'content')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['delete_selected']

    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at')
    search_fields = ('author__username', 'content')
