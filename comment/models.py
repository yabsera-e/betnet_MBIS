from django.db import models
from users.models import CustomUser

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, related_name="user_comments", null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'
