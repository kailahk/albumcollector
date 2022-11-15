from django.db import models

# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genres = models.CharField(max_length=200)
    release_year = models.IntegerField()
    track_list = models.TextField(max_length=250)
    list = models.CharField(max_length=100)

    def __str__(self):
        return self.title