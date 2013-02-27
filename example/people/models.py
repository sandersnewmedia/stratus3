from django.db import models
from django.utils.translation import ugettext_lazy as _


class Person(models.Model):
    name = models.CharField(_('name'), max_length=255)
    hobbies = models.TextField(_('hobbies'))
    is_active = models.BooleanField(_('active'))
    age = models.IntegerField(_('age'))
    likes = models.CommaSeparatedIntegerField(_('likes'), max_length=255)
    birth_date = models.DateTimeField(_('birth date'))
    avatar = models.ImageField(_('avatar'), upload_to='avatars')


class Team(models.Model):
    owner = models.ForeignKey(Person)
