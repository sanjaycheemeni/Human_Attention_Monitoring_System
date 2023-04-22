from django.db import models

# Create your models here.
class UserData(models.Model):
    user_name = models.CharField(max_length=60)
    user_mail = models.CharField(max_length=60)
    gender = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    age = models.CharField(max_length=5)


class Session(models.Model):
    session_key = models.CharField(max_length=8)
    host_id =  models.CharField(max_length=60)
    host_name = models.CharField(max_length=60)
    # start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)

class sessionLog(models.Model):
    session_key = models.CharField(max_length=8)
    user = models.CharField(max_length=60)
    mr = models.CharField(max_length=60)
    ear = models.CharField(max_length=60)
    time_ms = models.CharField(max_length=60)