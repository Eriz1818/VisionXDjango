from django.db import models


class UploadFile(models.Model):
    file = models.FileField(upload_to='files/images')


class TagFreq(models.Model):
    tag_Name = models.CharField(max_length=150, verbose_name='Tag Name')
    tag_freq = models.IntegerField(verbose_name='Tag Freq')

class TempTable(models.Model):
    TempTagName = models.CharField(max_length=150, verbose_name='Tag Name')
    TempTagFreq = models.IntegerField(verbose_name='Tag Freq')