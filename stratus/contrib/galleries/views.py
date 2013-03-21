from django.views.generic.base import ContextMixin

from stratus.contrib.galleries.models import ImageGallery


class ImageGalleryMixin(ContextMixin):
    gallery_keys = []

    def get_gallery_keys(self):
        return self.gallery_keys

    def get_galleries(self, *keys):
        galleries = ImageGallery.objects.filter(key__in=keys)
        galleries = galleries.prefetch_related('images__thumbnails__size')
        return dict((gallery.key, gallery) for gallery in galleries)

    def get_context_data(self, **kwargs):
        context = super(ImageGalleryMixin, self).get_context_data(**kwargs)

        gallery_keys = self.get_gallery_keys()
        galleries = self.get_galleries(*gallery_keys)
        context['galleries'] = galleries

        return context
