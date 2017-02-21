from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .validators import validate_file_extension, valid
# Create your models here.


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField(validators=[valid])

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.fk})
        #return reverse('music:index')

