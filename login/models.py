from django.db import models

# Create your models here.
class UserData(models.Model):
    user_name = models.CharField(max_length=60)
    user_mail = models.CharField(max_length=60)
    gender = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    age = models.CharField(max_length=5)



