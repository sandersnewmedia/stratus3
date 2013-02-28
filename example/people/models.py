from django.db import models
from django.utils.translation import ugettext_lazy as _


class Person(models.Model):
    name = models.CharField(_('name'), max_length=255)
    order = models.IntegerField(_('order'))


class Image(models.Model):
    person = models.ForeignKey(Person, verbose_name=_('person'))
    image = models.ImageField(_('image'), upload_to='people/images/', blank=True)
    caption = models.TextField(_('caption'))
    order = models.IntegerField(_('order'))
