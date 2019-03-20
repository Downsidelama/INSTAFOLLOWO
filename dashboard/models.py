from django.db import models


# Create your models here.

class InstagramAccount(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    started = models.BooleanField()
    run_type = models.CharField(max_length=20)
    hashtag = models.CharField(max_length=150)
    other_profile = models.CharField(max_length=150)
