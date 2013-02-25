import re

from django import forms
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline
from django.contrib.admin.views.main import ERROR_FLAG
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.encoding import force_unicode
from django.utils.html import escape, escapejs
from django.utils.translation import ugettext as _

from stratus import widgets
from stratus.templatetags.stratus_static import static


class StratusModelAdmin(ModelAdmin):
    delete_selected_confirmation_template = 'stratus/delete_selected_confirmation.html'

    def __init__(self, *args, **kwargs):
        super(StratusModelAdmin, self).__init__(*args, **kwargs)

        self.name = self.opts.module_name.title()
        self.info = [self.opts.app_label, self.opts.module_name]

        self.formfield_overrides.update({
            models.DateTimeField: {
                'form_class': forms.SplitDateTimeField,
                'widget': widgets.StratusAdminSplitDateTime,
            },
            models.DateField: {'widget': widgets.StratusAdminDateWidget},
            models.TimeField: {'widget': widgets.StratusAdminTimeWidget},
        })

    def change_url(self):
        return reverse('stratus:{}_{}_changelist'.format(*self.info), current_app=self.admin_site.name)

    def add_url(self):
        return reverse('stratus:{}_{}_add'.format(*self.info), current_app=self.admin_site.name)

    def get_context_data(self, request):
        return {
            'page': self,
        }

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        self.add_form_template = self.change_form_template = (
            'stratus/{}/{}/change_form.html'.format(*self.info),
            'stratus/{}/change_form.html'.format(*self.info),
            'stratus/change_form.html',
        )

        context.update(self.get_context_data(request))

        return super(StratusModelAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    def changelist_view(self, request, extra_context=None):
        if ERROR_FLAG in request.GET:
            return render(request, 'stratus/invalid_setup.html', {
                'title': _('Database error'),
            })

        self.change_list_template = (
            'stratus/{}/{}/change_list.html'.format(*self.info),
            'stratus/{}/change_list.html'.format(*self.info),
            'stratus/change_list.html'
        )

        context = self.get_context_data(request)
        context.update(extra_context or {})

        return super(StratusModelAdmin, self).changelist_view(request, context)

    def delete_view(self, request, object_id, extra_context=None):
        self.delete_confirmation_template = (
            'stratus/{}/{}/delete_confirmation.html'.format(*self.info),
            'stratus/{}/delete_confirmation.html'.format(*self.info),
            'stratus/delete_confirmation.html'
        )

        context = self.get_context_data(request)
        context.update(extra_context or {})

        return super(StratusModelAdmin, self).delete_view(request, object_id, context)

    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Note: This is a ugly copy/paste hack. We just need to change the
        namespace on the reverse calls :(.
        Determines the HttpResponse for the add_view stage.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj)}
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if "_continue" in request.POST:
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if "_popup" in request.POST:
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if "_popup" in request.POST:
            return HttpResponse(
                '<!DOCTYPE html><html><head><title></title></head><body>'
                '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script></body></html>' %
                # escape() calls force_unicode.
                (escape(pk_value), escapejs(obj)))
        elif "_addanother" in request.POST:
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)

            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            if self.has_change_permission(request, None):
                post_url = reverse('status:%s_%s_changelist' %
                                   (opts.app_label, opts.module_name),
                                   current_app=self.admin_site.name)
            else:
                post_url = reverse('stratus:index',
                                   current_app=self.admin_site.name)
            return HttpResponseRedirect(post_url)

    def response_change(self, request, obj):
        """
        Note: This is a ugly copy/paste hack. We just need to change the
        namespace on the reverse calls :(.
        Determines the HttpResponse for the change_view stage.
        """
        opts = obj._meta

        # Handle proxy models automatically created by .only() or .defer().
        # Refs #14529
        verbose_name = opts.verbose_name
        module_name = opts.module_name
        if obj._deferred:
            opts_ = opts.proxy_for_model._meta
            verbose_name = opts_.verbose_name
            module_name = opts_.module_name

        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {'name': force_unicode(verbose_name), 'obj': force_unicode(obj)}
        if "_continue" in request.POST:
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if "_popup" in request.REQUEST:
                return HttpResponseRedirect(request.path + "?_popup=1")
            else:
                return HttpResponseRedirect(request.path)
        elif "_saveasnew" in request.POST:
            msg = _('The %(name)s "%(obj)s" was added successfully. You may edit it again below.') % {'name': force_unicode(verbose_name), 'obj': obj}
            self.message_user(request, msg)
            return HttpResponseRedirect(reverse('stratus:%s_%s_change' %
                                        (opts.app_label, module_name),
                                        args=(pk_value,),
                                        current_app=self.admin_site.name))
        elif "_addanother" in request.POST:
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(verbose_name)))
            return HttpResponseRedirect(reverse('stratus:%s_%s_add' %
                                        (opts.app_label, module_name),
                                        current_app=self.admin_site.name))
        else:
            self.message_user(request, msg)
            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            if self.has_change_permission(request, None):
                post_url = reverse('stratus:%s_%s_changelist' %
                                   (opts.app_label, module_name),
                                   current_app=self.admin_site.name)
            else:
                post_url = reverse('stratus:index',
                                   current_app=self.admin_site.name)
            return HttpResponseRedirect(post_url)

    @property
    def media(self):
        media = super(StratusModelAdmin, self).media
        admin_base = r'^{}'.format(static('admin'))
        stratus_base = static('stratus')
        media._js = [re.sub(admin_base, stratus_base, path) for path in media._js]
        return media


class StratusStackedInline(StackedInline):
    template = 'stratus/edit_inline/stacked.html'


class StratusTabularInline(TabularInline):
    template = 'stratus/edit_inline/tabular.html'
