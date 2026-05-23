
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.

# User = get_user_model()


class Post(models.Model):
    """
    this is a class to define posts for blog app
    """

    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField(default=False)
    category = models.ManyToManyField("Category", null=True)
    tag = models.ManyToManyField("Tag", null=True)
    #view_count
    #comment_count
    

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    class Meta:
        ordering = ['-view_count','-comment_count','published_date']

    def __str__(self):
        return self.title

    def get_snippets(self):
        words = self.content.split()
        return " ".join(words[:5])

    def get_absolute_api_url(self):
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
