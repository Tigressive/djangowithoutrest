from django.db import models


# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
