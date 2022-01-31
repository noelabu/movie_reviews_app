from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
  


# Create your models here.


class BookmarkedReviews(models.Model):
    user = models.CharField( max_length=255)
    reviews = models.JSONField()

    def __str__(self):
        return self.user

