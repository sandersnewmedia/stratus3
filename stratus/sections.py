from django.conf.urls import include, patterns, url
from django.db import models

from stratus.exceptions import AlreadyRegistered, NotRegistered
from stratus.pages import StratusModelAdminPage
from stratus.utils import nameify


class StratusSection(object):
    namespace = None
    include_in_nav = True

    def __init__(self, site, name=None):
        self.site = site
        self.name = name or self.namespace or nameify(self, 'Section')
        self._registry = {}

    def register(self, cls, namespace=None):
        instance = cls(self.site, section=self, name=namespace)

        if instance.name in self._registry:
            raise AlreadyRegistered("'{}' has already been "
                "registered.".format(instance.name))

        self._registry[instance.name] = instance

        return instance

    def unregister(self, cls, namespace=None):
        instance = cls(self.site, section=self, name=namespace)

        if instance.name not in self._registry:
            raise NotRegistered("'{}' has not been "
                "registered.".format(instance.name))

        del self._registry[instance.name]

    def get_urls(self):
        urlpatterns = patterns('')

        for page in self._registry.itervalues():
            urlpatterns += page.get_urlpatterns()

        return urlpatterns

    def get_urlpatterns(self):
        return patterns('', url(r'^{}/'.format(self.name), include(self.get_urls())))

    @property
    def nav(self):
        return [page for page in self._registry.itervalues() if page.include_in_nav]

    @property
    def url(self):
        try:
            return self.nav[0].url
        except IndexError:
            return None


class StratusAppSection(StratusSection):
    app_label = None

    def __init__(self, *args, **kwargs):
        if self.app_label is None:
            self.app_label = self.__class__.__module__.split('.')[-2]

        super(StratusAppSection, self).__init__(*args, **kwargs)

        for model in models.get_models(models.get_app(self.app_label)):
            attrs = {'model': model}
            ModelPage = type('{}Page'.format(model.__name__), (StratusModelAdminPage,), attrs)
            self.register(ModelPage)
