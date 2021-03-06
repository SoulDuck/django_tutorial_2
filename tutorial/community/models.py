# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Article(models.Model):
    name=models.CharField(max_length=30)
    title = models.CharField(max_length=40)
    contents = models.TextField()
    url = models.URLField()
    email = models.EmailField()
    cdate = models.DateTimeField(auto_now_add=True)

class UploadFile(models.Model):
    title = models.TextField(default='')
    file = models.FileField(null=True )#, upload_to='media'


