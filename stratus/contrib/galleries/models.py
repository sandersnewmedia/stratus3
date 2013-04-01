import os

from django.db import models
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from stratus.contrib.galleries.resizers import resizers
from stratus.validators import validate_key


class ImageGallery(models.Model):
    title = models.CharField(_('title'), max_length=100)
    key = models.CharField(_('key'), max_length=50, unique=True, validators=[validate_key])

    class Meta(object):
        db_table = 'stratus_imagegallery'
        verbose_name_plural = _('image galleries')

    def __unicode__(self):
        return self.title


def image_original_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    path = 'galleries/images/%(gallery)s/%(uid)s/_original%(ext)s' % {
        'gallery': instance.gallery.key,
        'uid': instance.uid,
        'ext': ext,
    }
    return path.lower()


def image_thumbnail_upload_to(instance, filename):
    path = 'galleries/images/%(gallery)s/%(uid)s/%(size)s.%(format)s' % {
        'gallery': instance.original.gallery.key,
        'uid': instance.original.uid,
        'size': instance.size.key,
        'format': 'jpg',
        'format': instance.size.format,
    }
    return path.lower()


class Image(models.Model):
    gallery = models.ForeignKey(ImageGallery, verbose_name=_('gallery'), related_name='images')
    uid = models.CharField(_('UID'), max_length=8, default=lambda: get_random_string(length=8), editable=False)
    image = models.ImageField(_('image'), upload_to=image_original_upload_to)
    order = models.PositiveIntegerField(_('order'), default=0)

    class Meta(object):
        db_table = 'stratus_image'
        unique_together = ['gallery', 'uid']
        ordering = ['order']

    def __unicode__(self):
        return self.image.name

    def thumbnailsdict(self):
        if not hasattr(self, '_cached_thumbnailsdict'):
            thumbnails = self.thumbnails.all()
            thumbnailsdict = dict((thumbnail.size.key, thumbnail) for thumbnail in thumbnails)
            self._cached_thumbnailsdict = thumbnailsdict
        return self._cached_thumbnailsdict


class ThumbnailSize(models.Model):
    FORMATS_JPEG = 'jpg'
    FORMATS = [
        ('jpg', 'JPEG'),
    ]

    gallery = models.ForeignKey(ImageGallery, verbose_name=_('gallery'), related_name='sizes')
    key = models.CharField(_('key'), max_length=50, validators=[validate_key])
    resizer = models.CharField(_('resizer'), max_length=128, choices=resizers.choices, default=resizers.default)
    format = models.CharField(_('format'), max_length=32, choices=FORMATS, default=FORMATS_JPEG)
    quality = models.PositiveIntegerField(_('quality'), default=85)
    width = models.PositiveIntegerField(_('width'), null=True)
    height = models.PositiveIntegerField(_('height'), null=True)

    class Meta(object):
        db_table = 'stratus_thumbnailsize'
        unique_together = ['gallery', 'key']

    def __unicode__(self):
        return '%s:%sx%s' % (self.key, self.width, self.height)

    def resize(self, original):
        resizer = resizers.get_resizer(self.resizer)(
            width=self.width,
            height=self.height,
            format=self.format,
            quality=self.quality,
        )
        return resizer.resize(original)


class Thumbnail(models.Model):
    original = models.ForeignKey(Image, verbose_name=_('original'), related_name='thumbnails')
    size = models.ForeignKey(ThumbnailSize, verbose_name=_('size'), related_name='thumbnails')
    image = models.ImageField(_('image'), upload_to=image_thumbnail_upload_to, width_field='width', height_field='height')
    width = models.PositiveIntegerField(_('width'), default=0)
    height = models.PositiveIntegerField(_('height'), default=0)

    class Meta(object):
        db_table = 'stratus_thumbnail'
        unique_together = ['original', 'size']

    def __unicode__(self):
        return self.image.name

    def resize(self, save=True):
        self.image.save(
            name=self.original.image.name,
            content=self.size.resize(self.original.image),
            save=save,
        )


@receiver(models.signals.post_save, sender=ImageGallery)
def create_default_sizes(sender, instance, created, **kwargs):
    if created:
        instance.sizes.create(key='admin', resizer='crop', width=200, height=200)


@receiver(models.signals.post_save, sender=ThumbnailSize)
def create_thumbnails_for_size(sender, instance, created, **kwargs):
    for image in instance.gallery.images.all():
        thumbnail, created = image.thumbnails.get_or_create(size=instance)
        thumbnail.resize()


@receiver(models.signals.post_save, sender=Image)
def create_thumbnails_for_original(sender, instance, created, **kwargs):
    for size in instance.gallery.sizes.all():
        thumbnail, created = instance.thumbnails.get_or_create(size=size)
        thumbnail.resize()
