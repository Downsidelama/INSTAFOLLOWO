from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class InstagramAccount(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    started = models.BooleanField()
    run_type = models.CharField(max_length=20)
    hashtag = models.CharField(max_length=150)
    other_profile = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
