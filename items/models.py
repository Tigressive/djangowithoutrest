from django.db import models
from django.contrib.auth.models import (User, PermissionsMixin, UserManager)


# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    isPrivate = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item", null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    borrowed_location = models.CharField(max_length=100)
    isBorrowed = models.BooleanField(null=True)
