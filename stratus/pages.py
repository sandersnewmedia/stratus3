from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

from stratus import conf
from stratus.admin import StratusModelAdmin
from stratus.utils import nameify
from stratus.views import StratusPageView


class StratusPage(object):
    namespace = None
    view_class = StratusPageView
    template_name = None
    include_in_nav = True
    login_required = True
    cacheable = False

    def __init__(self, site, section=None, name=None):
        self.site = site
        self.section = section
        self.name = name or self.namespace or nameify(self, 'Page')
        self.view = self.get_view()

    def wrap_view(self, view):
        if not self.cacheable:
            view = never_cache(view)

        if self.login_required:
            view = login_required(login_url=conf.get('STRATUS_LOGIN_URL'))(view)

        return view

    def get_view(self):
        return self.wrap_view(self.view_class.as_view(page=self))

    def get_urls(self):
        if self.section:
            name = '{}_{}'.format(self.name, self.section.name)
        else:
            name = self.name
        return [url(r'^{}/$'.format(self.name), self.view, name=name)]

    def get_urlpatterns(self):
        return patterns('', *self.get_urls())

    def get_context_data(self, request):
        return {
            'request': request,
            'site': self.site,
            'page': self,
        }

    def render(self, request, template_name=None, extra_context=None):
        ctx = self.get_context_data(request)
        ctx.update(extra_context or {})
        return render(request, template_name or self.template_name, ctx)

    @property
    def url(self):
        if self.section:
            name = '{}:{}_{}'.format(self.site.app_name, self.name, self.section.name)
        else:
            name = '{}:{}'.format(self.site.app_name, self.name)
        return reverse(name, current_app=self.site.name)


class StratusModelAdminPage(StratusPage):
    model = None
    admin_class = StratusModelAdmin

    def __init__(self, *args, **kwargs):
        super(StratusModelAdminPage, self).__init__(*args, **kwargs)
        admin_site = admin.AdminSite(name=self.site.name, app_name=self.site.app_name)
        self.model_admin = self.admin_class(self.model, admin_site, page=self)

    def get_urls(self):
        app = self.model._meta.app_label
        name = self.model._meta.module_name

        urlpatterns = patterns('',
            url(
                regex=r'^{}/$'.format(name),
                view=self.wrap_view(self.model_admin.changelist_view),
                name='{}_{}_changelist'.format(app, name),
            ),
            url(
                regex=r'^{}/add/$'.format(name),
                view=self.wrap_view(self.model_admin.add_view),
                name='{}_{}_add'.format(app, name),
            ),
            url(
                regex=r'^{}/(.+)/history/$'.format(name),
                view=self.wrap_view(self.model_admin.history_view),
                name='{}_{}_history'.format(app, name),
            ),
            url(
                regex=r'^{}/(.+)/delete/$'.format(name),
                view=self.wrap_view(self.model_admin.delete_view),
                name='{}_{}_delete'.format(app, name),
            ),
            url(
                regex=r'^{}/(.+)/$'.format(name),
                view=self.wrap_view(self.model_admin.change_view),
                name='{}_{}_change'.format(app, name),
            ),
        )

        return urlpatterns

    @property
    def url(self):
        name = '{}:{}_{}_changelist'.format(
            self.site.app_name,
            self.model._meta.app_label,
            self.model._meta.module_name,
        )
        return reverse(name, current_app=self.site.name)
