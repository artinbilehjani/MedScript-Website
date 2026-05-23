from django.contrib import admin
from blog.models import Post,Category,Tag,Comment,PostFile
# Register your models here.

class PostAdmin(admin.ModelAdmin):
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
    list_display = [
        "display_name",
        "approved",
        "created_date",
    ]

    list_filter = ("approved",)




admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostFile)
