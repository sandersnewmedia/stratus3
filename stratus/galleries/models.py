import os

from django.db import models
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from stratus.galleries.strategies import strategies


class ImageGallery(models.Model):
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    # TODO add max allowed images field

    class Meta(object):
        db_table = 'stratus_imagegallery'
        verbose_name_plural = _('image galleries')

    def __unicode__(self):
        return self.title


def image_original_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    path = 'galleries/images/%(gallery)s/%(uid)s/_original%(ext)s' % {
        'gallery': instance.gallery.slug,
        'uid': instance.uid,
        'ext': ext,
    }
    return path.lower()


def image_thumbnail_upload_to(instance, filename):
    path = 'galleries/images/%(gallery)s/%(uid)s/%(size)s.%(format)s' % {
        'gallery': instance.original.gallery.slug,
        'uid': instance.original.uid,
        'size': instance.size.slug,
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
            thumbnails = dict((thumbnail.size.slug, thumbnail) for thumbnail in self.thumbnails.all())
            self._cached_thumbnailsdict = thumbnails
        return self._cached_thumbnailsdict


class ThumbnailSize(models.Model):
    FORMATS_JPEG = 'jpg'
    FORMATS = [
        ('jpg', 'JPEG'),
    ]

    gallery = models.ForeignKey(ImageGallery, verbose_name=_('gallery'), related_name='sizes')
    slug = models.SlugField(_('slug'))
    strategy = models.CharField(_('strategy'), max_length=128, choices=strategies.choices, default=strategies.default)
    format = models.CharField(_('format'), max_length=32, choices=FORMATS, default=FORMATS_JPEG)
    quality = models.PositiveIntegerField(_('quality'), default=85)
    width = models.PositiveIntegerField(_('width'), null=True)
    height = models.PositiveIntegerField(_('height'), null=True)
    auto_created = models.BooleanField(_('auto created'), default=False, help_text=_('Is set when the size was created by the system.'), editable=False)

    class Meta(object):
        db_table = 'stratus_imagesize'
        unique_together = ['gallery', 'slug']

    def __unicode__(self):
        return '%s:%sx%s' % (self.slug, self.width, self.height)

    def resize(self, original):
        strategy = strategies.get_strategy(self.strategy)(
            width=self.width,
            height=self.height,
            format=self.format,
            quality=self.quality,
        )
        return strategy.resize(original)


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
        instance.sizes.create(slug='admin', strategy='crop', width=200, height=200, auto_created=True)


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
