from django.db import models

# Create your models here.

class Comment(models.Model):
    """class for comments of each post"""
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE) 
    display_name = models.CharField(max_length=50)
    message = models.TextField(max_length=255)
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.display_name

    def get_snippets(self):
        words = self.message.split()
        snippet = " ".join(words[:5])
        if len(words) > 5:
            snippet += "..."
        return snippet
    
    @property
    def like_count(self):
        return self.votes.filter(vote_type='like').count()
    
    @property
    def dislike_count(self):
        return self.votes.filter(vote_type='dislike').count()