from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

HOURS_CHOICES = (
    ("1","a full day"),
    ("0.5", "half a day"),
)


def get_full_name(self):
    full_name = self.first_name + ' ' + self.last_name
    return full_name

User.add_to_class("__str__", get_full_name)


class Project(models.Model):
    projectName = models.CharField("Project name", max_length=255)

    def __str__(self):
        return (self.projectName)

class WorkDay(models.Model):
    date = models.DateField("Date")
    project = models.ForeignKey('Project')
    hours = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2)
    days = models.CharField(max_length=255, choices = HOURS_CHOICES)
    user = models.ForeignKey(User)
