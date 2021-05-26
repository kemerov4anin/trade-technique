from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Albums(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=False, db_column='userId')
    title = models.CharField(max_length=255, null=False, blank=False)


class Photos(models.Model):
    albumId = models.ForeignKey('Albums', on_delete=models.SET_NULL, null=True, blank=True, db_column='albumId',
                                related_name='photos')
    title = models.CharField(max_length=255, null=False, blank=False)
    url = models.URLField(null=False, blank=False)
    thumbnailUrl = models.URLField(null=False, blank=False)
    localUrl = models.CharField(max_length=1000, blank=True)

