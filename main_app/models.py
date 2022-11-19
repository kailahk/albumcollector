from django.db import models
from django.urls import reverse
from datetime import date, timedelta

TIMES_OF_DAY = (
    ('M', 'Morning (5am-11am)'),
    ('D', 'Day (11am-5pm)'),
    ('E', 'Evening (5pm-11pm)'),
    ('N', 'Night (11pm-5am)'),
)

# Create your models here.
class List(models.Model):
    name = models.CharField(max_length=55)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lists_detail', kwargs={'pk':self.id})

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genres = models.CharField(max_length=200)
    release_year = models.IntegerField()
    track_list = models.TextField(max_length=500)
    lists = models.ManyToManyField(List)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'album_id': self.id})

    def listened_within_a_week(self):
        today = date.today()
        week_ago = today - timedelta(days=7)
        return self.listen_set.filter(date__gt=week_ago).exists()

class Listen(models.Model):
    date = models.DateField()
    timeofday = models.CharField(
        'Time of Day',
        max_length=1,
        choices=TIMES_OF_DAY,
        default=TIMES_OF_DAY[1][0]
    )

    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_timeofday_display()} on {self.date}'

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return f'Album Cover for album_id: {self.album_id} @{self.url}'