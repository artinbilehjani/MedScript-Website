from django.contrib import admin
from blog.models import Post,Category,Tag,Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "title",
        "status",
        "category",
        "created_date",
        "published_date",
    ]

    list_filter = [
        "author",
        "status",
    ]

class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "approved",
        "created_date",
    ]

    list_filter = ("approved",)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CategoryAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag,TagAdmin)