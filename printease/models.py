from django.db import models
from django.urls import reverse


class PrintEaseSignModel(models.Model):

    username = models.CharField(max_length=100),
    email = models.EmailField(max_length=254),
    password = models.CharField(max_length=200),

    def get_absolute_url(self):
        return reverse("index")


class FilesUpload(models.Model):
    file = models.FileField()
