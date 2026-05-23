from django import forms
from .models import Post
from django.utils import timezone


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content", "status", "category", "published_date"]
        widgets = {
            "published_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M:%S",  # فرمت مورد انتظار برای datetime-local
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اگر فرم در حالت ویرایش نباشد (یعنی آبجکت جدیدی در حال ایجاد است)،
        # تاریخ پیش‌فرض را روی زمان فعلی تنظیم کن
        if not self.instance.pk:
            self.fields["published_date"].initial = timezone.now()