from StringIO import StringIO

from django.core.files.base import ContentFile

from PIL import Image, ImageOps


def normalize_format(format):
    if format.upper() == 'JPG':
        return 'JPEG'
    return format.upper()


class StrategyRegistry(object):
    default = None

    def __init__(self):
        self._registry = {}

    @property
    def choices(self):
        strategies = sorted(self._registry.iteritems())
        return [(key, name) for key, (name, strategy) in strategies]

    def register(self, key, name, strategy, default=False):
        self._registry[key] = (name, strategy)
        if default:
            self.default = key

    def get_strategy(self, key):
        name, strategy = self._registry[key]
        return strategy


class BaseStrategy(object):

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


class CropStrategy(BaseStrategy):

    def _resize(self, source):
        return ImageOps.fit(source, (self.width, self.height), Image.ANTIALIAS)


strategies = StrategyRegistry()
strategies.register('crop', 'Crop', CropStrategy, default=True)
