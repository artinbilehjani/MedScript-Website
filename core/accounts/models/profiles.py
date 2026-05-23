from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from .users import User

class Profile(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50,default="medscript")
    image = models.ImageField(upload_to='images/profile_pictures/', default='images/default_images/blank_profile_picture.png')
    description = models.TextField(null=True,blank=True)
    post_count = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

