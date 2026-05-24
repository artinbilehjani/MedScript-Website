from django.contrib import admin
from blog.models import Post,Category,Tag,Comment,PostFile
# Register your models here.


class PostFileInline(admin.TabularInline):
    model = PostFile

class PostAdmin(admin.ModelAdmin):
    inlines = [
        PostFileInline,
    ]
    list_display = [
        "author",
        "title",
        "status",
        "created_date",
        "published_date",
    ]

    list_filter = [
        "author",
        "status",
    ]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter_name', 'post', 'is_approved', 'created_date')
    list_filter = ('is_approved', 'created_date')
    search_fields = ('user__username', 'content', 'post__title')

    def commenter_name(self, obj):
        return obj.user.profile.display_name if hasattr(obj.user, 'profile') else obj.user.username

    commenter_name.short_description = 'کاربر'



admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostFile)
