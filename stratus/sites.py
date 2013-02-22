from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

from stratus import conf
from stratus.exceptions import AlreadyRegistered, NotRegistered


class StratusSite(object):

    def __init__(self, name='stratus', app_name='stratus'):
        self.name = name
        self.app_name = app_name
        self._registry = {}

    def register(self, cls, namespace=None):
        instance = cls(self, name=namespace)

        if instance.name in self._registry:
            raise AlreadyRegistered("'{}' has already been "
                "registered.".format(instance.name))

        self._registry[instance.name] = instance

        return instance

    def unregister(self, cls, namespace=None):
        instance = cls(self, name=namespace)

        if instance.name not in self._registry:
            raise NotRegistered("'{}' has not been "
                "registered.".format(instance.name))

        del self._registry[instance.name]

    @property
    def urls(self):
        urlpatterns = patterns('',
            url(r'^$', RedirectView.as_view(url=conf.get('STRATUS_BASE_URL')), name='index'),
        )

        for obj in self._registry.itervalues():
            urlpatterns += obj.get_urlpatterns()

        return (urlpatterns, self.app_name, self.name)

    @property
    def nav(self):
        nav = []
        for obj in self._registry.itervalues():
            if hasattr(obj, 'nav'):
                nav.append({
                    'main': obj,
                    'sub': obj.nav,
                })
            else:
                if obj.include_in_nav:
                    nav.append({
                        'main': obj,
                        'sub': [],
                    })
        return nav

site = StratusSite()
