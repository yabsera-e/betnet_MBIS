from django.db import models
from users.models import CustomUser
from listing.models import Listing

class Conversation(models.Model):
    participants = models.ManyToManyField(CustomUser, related_name="conversations")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='conversations', blank=True, null=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name="authored_messages", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
