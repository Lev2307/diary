from django.db import models
from django.contrib.auth.models import User


class VerifyAccModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    ip_address = models.CharField(max_length=16)