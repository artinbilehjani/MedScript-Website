
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from hitcount.models import HitCount,HitCountMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify

# Create your models here.



class Post(models.Model):
    """
    this is a class to define posts for blog app
    """
    author = models.ForeignKey("accounts.Profile", on_delete=models.SET_NULL,null=True,blank=True)
    image = models.ImageField(upload_to='images/post_thumbnails/', default='images/default_images/blank_post_thumbnail.png')
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField(default=False)
    category = models.ManyToManyField("Category",)
    tag = models.ManyToManyField("Tag",)
    links = models.TextField(null=True,blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
 related_query_name='hit_count_generic_relation')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()
    slug = models.SlugField(editable=False,unique=True, max_length=255)

    class Meta:
        ordering = ['published_date']

    def __str__(self):
        return self.title

    def _generate_unique_slug(self):
        base_slug = slugify(self.title, allow_unicode=True) or "post"
        max_length = self._meta.get_field("slug").max_length

        base_slug = base_slug[:max_length]
        slug = base_slug
        counter = 1

        while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            suffix = f"-{counter}"
            trimmed_base = base_slug[: max_length - len(suffix)]
            slug = f"{trimmed_base}{suffix}"
            counter += 1

        return slug

    def save(self, *args, **kwargs):
        self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def get_snippets(self):
        words = self.content.split()
        snippet = " ".join(words[:5])
        if len(words) > 5:
            snippet += "..."
        return snippet

    def get_absolute_api_url(self):
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})


class Category(models.Model):
    """class for category query"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    """class for tag query"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class PostFile(models.Model):
    file = models.FileField(upload_to="files/", blank=True, null=True) # Initial upload_to, will be overridden
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='files')

    def save(self, *args, **kwargs):
        # Check if the instance is being created for the first time
        if self.pk is None:
            # Save the instance first to get the post.id if it's newly created
            super().save(*args, **kwargs)

            # Construct the new upload path using post.id
            # Ensure post and post.id are not None
            if self.post and self.post.id:
                new_upload_path = f"files/{self.post.id}/"
                self.file.upload_to = new_upload_path
                super().save(*args, **kwargs) # Save again with the updated upload_to path
            else:
                # Handle cases where post or post.id might be missing, though FK should prevent this
                super().save(*args, **kwargs)
        else:
            # If not being created, just save normally
            super().save(*args, **kwargs)

