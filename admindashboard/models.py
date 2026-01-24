from django.db import models
from users.models import CustomUser

class Position(models.TextChoices):
    MAIN = "main"
    DETAIL_PAGE = "detail_page"

class Ads(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL, null=True, blank=True, related_name='ads_posted')
    company_name = models.CharField(max_length=100, blank=True, null=True)
    file_path = models.TextField()
    media_type = models.TextField(null=True, blank=True)
    duration = models.IntegerField()
    position = models.CharField(max_length=50, choices=Position.choices)
    expire_date = models.DateField()
    fee = models.CharField(max_length=100, null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ads'