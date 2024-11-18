from django.db import models
from user.models import Account

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="departments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
