from django.db import models
from django.conf import settings

class ChatMessage(models.Model):
    """
    Stores chat history for each user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_reply = models.TextField()
    intent = models.CharField(max_length=128, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)  # optional: store model scores, entities
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"ChatMessage(user={self.user}, intent={self.intent}, at={self.created_at.isoformat()})"
