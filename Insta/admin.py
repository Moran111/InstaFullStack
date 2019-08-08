from django.contrib import admin

from Insta.models import InstaUser, Like, Post, UserConnection, Comment

class FollowingInline(admin.StackedInline):
    model = UserConnection
    fk_name = 'creator'

class FollowerInline(admin.StackedInline):
    model = UserConnection
    fk_name = 'following'

class UserAdmin(admin.ModelAdmin):
    inlines = [
        FollowerInline,
        FollowingInline,
    ]

class CommentInline(admin.StackedInline):
    model = Comment

class LikeInline(admin.StackedInline):
    model = Like

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
        LikeInline,
    ]

# Register your models here.
admin.site.register(Post)
admin.site.register(InstaUser, UserAdmin)
admin.site.register(Like)
admin.site.register(UserConnection)
admin.site.register(Comment)
