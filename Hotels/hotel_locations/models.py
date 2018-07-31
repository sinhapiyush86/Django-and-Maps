from django.db import models

# Create your models here.
class Details_Table(models.Model):
    name = models.CharField(max_length=40)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    urls = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    def __str__(self):
        return self.name
