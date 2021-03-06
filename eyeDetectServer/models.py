from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Record(models.Model):
    time = models.IntegerField()
    user = models.CharField(max_length=30, default="hgod")
    blink = models.IntegerField(default=1)
    EAR = models.FloatField(default=0)
    threshold = models.FloatField(default=-1)
    index = models.IntegerField(default=-1)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.timestamp.strftime("%Y/%m/%d %H:%M:%S")

# class ColorRecord(models.Model):
#     user_id = models.IntegerField()
#     record = models.JSONField()