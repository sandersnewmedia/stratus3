from functools import update_wrapper

from django.conf.urls import patterns
from django.contrib import admin
from django.shortcuts import render


class StratusAdminSite(admin.sites.AdminSite):

    def __init__(self, *args, **kwargs):
        super(StratusAdminSite, self).__init__(*args, **kwargs)
        self._plugins = {}

    def update(self, site):
        self._registry.update(dict(site._registry))

    def get_urls(self):
        urlpatterns = patterns('')

        for plugin in self._plugins.itervalues():
            urlpatterns += plugin.get_urls()

        urlpatterns += super(StratusAdminSite, self).get_urls()

        return urlpatterns

    def register_plugin(self, plugin):
        self._plugins[plugin] = plugin(self)

    def unregister_plugin(self, plugin):
        if plugin in self._plugins:
            del self._plugins[plugin]


class StratusPlugin(object):

    def __init__(self, admin_site):
        self.admin_site = admin_site

    def wrap_view(self, view, cacheable=False):
        def wrapper(*args, **kwargs):
            return self.admin_site.admin_view(view, cacheable)(*args, **kwargs)
        return update_wrapper(wrapper, view)

    def render(self, request, template_name, context=None):
        context = context or {}
        context.update({'current_app': self.admin_site.name})
        return render(request, template_name, context)


site = StratusAdminSite()
