from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Profile,Position

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "is_superuser", "is_active","position")
    list_filter = ("username", "is_superuser", "is_active","position")
    searching_fields = ("username",)
    ordering = ("username",)

    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("username", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": ("is_staff", "is_superuser", "is_active"),
            },
        ),
        (
            "group permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "important dates",
            {
                "fields": ("last_login",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "position",
                ),
            },
        ),
    )


admin.site.register(Profile)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Position)