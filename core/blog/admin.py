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



class CategoryInline(admin.TabularInline):
    model = Category
    fk_name = "parent"
    fields = ("name",)
    extra = 1
    show_change_link = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "depth")
    inlines = [CategoryInline]

    def depth(self, obj):
        level = 1
        current = obj.parent
        while current:
            level += 1
            current = current.parent
        return level

    depth.short_description = "Level"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            qs = Category.objects.all()
            qs = qs.exclude(parent__parent__isnull=False)
            kwargs["queryset"] = qs
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag)
admin.site.register(PostFile)
