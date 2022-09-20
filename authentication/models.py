from django.db import models
import datetime
from django.contrib.auth.models import User


class VerifyDeviceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    os_name = models.CharField(max_length=35)
    browser = models.CharField(max_length=35)
    created_time = models.DateTimeField(default=datetime.datetime.now)