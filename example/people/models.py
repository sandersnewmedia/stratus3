from django.db import models
from django.utils.translation import ugettext_lazy as _


class Avatar(models.Model):
    image = models.ImageField(_('image'), upload_to='people/avatars/', blank=True)


class Person(models.Model):
    name = models.CharField(_('name'), max_length=255, help_text='help me')
    birthdate = models.DateTimeField(_('birth date'))
    avatars = models.ManyToManyField(Avatar, verbose_name=_('avatars'), blank=True)
    order = models.IntegerField(_('order'), default=1)

    class Meta(object):
        verbose_name_plural = _('people')


class Image(models.Model):
    person = models.ForeignKey(Person, verbose_name=_('person'))
    image = models.ImageField(_('image'), upload_to='people/images/')
    caption = models.CharField(_('caption'), max_length=255)
    order = models.IntegerField(_('order'), default=1)


class Team(models.Model):
    name = models.CharField(_('name'), max_length=255)
    members = models.ManyToManyField(Person, verbose_name=_('members'))
