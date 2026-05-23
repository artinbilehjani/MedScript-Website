from django.db import models
from django.contrib.auth.models import User

#for get absolute urls
from django.urls import reverse
from .posts import Post
#for taggit
from taggit.managers import TaggableManager

# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE) 
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0) 
    dislike_count = models.IntegerField(default=0) 
    created_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_date','like_count']

    def __str__(self):
        return self.name
