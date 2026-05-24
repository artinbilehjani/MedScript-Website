from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Comment(models.Model):
    """class for comments of each post"""
    post = models.ForeignKey(
        "blog.Post",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )
    message = models.TextField(max_length=255)
    is_approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f"{self.user} - {self.get_snippets()}"

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
    
class CommentReaction(models.Model):
    class ReactionType(models.TextChoices):
        LIKE = "like", _("Like")
        DISLIKE = "dislike", _("Dislike")

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="reactions",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="comment_reactions",
    )
    reaction = models.CharField(
        max_length=10,
        choices=ReactionType.choices,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["comment", "user"],
                name="unique_comment_user_reaction",
            )
        ]

    def __str__(self):
        return f"{self.user} -> {self.comment_id} ({self.reaction})"