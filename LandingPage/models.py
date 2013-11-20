from django.db import models

class Log(models.Model):
    logDateTime = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=20,default='')
    text = models.CharField(max_length=100,default='')
