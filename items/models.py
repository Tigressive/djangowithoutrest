from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
