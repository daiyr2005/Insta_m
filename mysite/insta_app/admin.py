from django.contrib import admin
from django.contrib import admin
from .models import (
    UserProfile, Follow, Hashtag, Post, Content,
    PostLike, Comment, CommentLike, SavePost, SavePostItem, Stories
)


class ContentInline(admin.TabularInline):
    model = Content
    extra = 1


class SavePostItemInline(admin.TabularInline):
    model = SavePostItem
    extra = 1


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'date_registered', 'followers_count', 'following_count']
    list_filter = ['date_registered']
    search_fields = ['user__username', 'user__email', 'bio']
    readonly_fields = ['date_registered']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_date']
    list_filter = ['created_date']
    search_fields = ['follower__user__username', 'following__user__username']


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['hashtag_name']
    search_fields = ['hashtag_name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_date', 'likes_count', 'comments_count']
    list_filter = ['created_date']
    search_fields = ['user__user__username', 'description']
    filter_horizontal = ['hashtag', 'people']
    inlines = [ContentInline]
    readonly_fields = ['created_date']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['post', 'file']
    list_filter = ['post__created_date']


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'like', 'created_date']
    list_filter = ['like', 'created_date']
    search_fields = ['user__user__username', 'post__description']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'text_preview', 'created_date', 'likes_count']
    list_filter = ['created_date']
    search_fields = ['user__user__username', 'text']
    readonly_fields = ['created_date']

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'like', 'created_date']
    list_filter = ['like', 'created_date']


@admin.register(SavePost)
class SavePostAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_date']
    inlines = [SavePostItemInline]


@admin.register(SavePostItem)
class SavePostItemAdmin(admin.ModelAdmin):
    list_display = ['save_post', 'post', 'created_date']
    list_filter = ['created_date']


@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_date']
    list_filter = ['created_date']
    search_fields = ['user__user__username']

# Register your models here.
