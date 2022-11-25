from django.db import models

class Item(models.Model):
    name = models.CharField(blank=True, max_length=255)
    disappeared_time = models.DateTimeField(blank=True, null=True)
    disappeared_count = models.IntegerField(blank=True, null=True)
    link = models.CharField(blank=True, null=True, max_length=255)
    


