from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    projectName = models.CharField("Project name", max_length=255)

    def __str__(self):
        return (self.projectName)

class WorkDay(models.Model):
    date = models.DateField("Date")
    project = models.ForeignKey('Project')
    hours = models.FloatField()
    user = models.ForeignKey(User)
