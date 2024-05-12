# oauth_integration/models.py

from django.db import models


class User(models.Model):
    user_id = models.IntegerField(unique=True)
    email = models.EmailField()
    login = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=200,blank=True)
    token_access = models.CharField(max_length=200,blank=True)
    is_available = models.BooleanField(default=False)
    username = models.CharField(default="Bonawara",max_length=50)
    def __str__(self):
        return self.login
