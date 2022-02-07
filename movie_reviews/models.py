from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
  


# Create your models here.


class BookmarkedReviews(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        to_field="username",
        on_delete=models.CASCADE,
    )
    folder = models.CharField(
        max_length=30,
        default='Favorites'
        )
    reviews = models.JSONField()

    def __str__(self):
        return self.user

