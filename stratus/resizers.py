from StringIO import StringIO

from django.core.files.base import ContentFile

from PIL import Image, ImageOps


def normalize_format(format):
    if format.upper() == 'JPG':
        return 'JPEG'
    return format.upper()


class ResizerRegistry(object):
    default = None

    def __init__(self):
        self._registry = {}

    @property
    def choices(self):
        resizers = sorted(self._registry.iteritems())
        return [(key, name) for key, (name, resizer) in resizers]

    def register(self, key, name, resizer, default=False):
        self._registry[key] = (name, resizer)
        if default:
            self.default = key

    def get_resizer(self, key):
        name, resizer = self._registry[key]
        return resizer


class BaseResizer(object):

    def __init__(self, width, height, format, quality):
        self.width = width
        self.height = height
        self.format = normalize_format(format)
        self.quality = quality

    def resize(self, source):
        source.seek(0)
        source = Image.open(source)
        source.convert('RGB')

        resized = self._resize(source)

        buf = StringIO()
        resized.save(buf, format=self.format, quality=self.quality)

        return ContentFile(buf.getvalue())


class CropResizer(BaseResizer):

    def _resize(self, source):
        return ImageOps.fit(source, (self.width, self.height), Image.ANTIALIAS)


resizers = ResizerRegistry()
resizers.register('crop', 'Crop', CropResizer, default=True)
