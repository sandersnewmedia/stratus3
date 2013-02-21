from django.db import models
from django.utils.translation import ugettext_lazy as _


class Person(models.Model):
    name = models.CharField(_('name'), max_length=255)


class Team(models.Model):
    owner = models.ForeignKey(Person)
