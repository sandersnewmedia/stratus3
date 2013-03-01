from functools import update_wrapper

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.text import capfirst


class StratusAdminSite(admin.AdminSite):

    def admin_view(self, view, cacheable=False):
        func = super(StratusAdminSite, self).admin_view(view, cacheable)

        def wrapper(request, *args, **kwargs):
            response = func(request, *args, **kwargs)
            try:
                response.context_data.update({
                    'navigation': self.get_navigation(request, *args, **kwargs),
                })
            except AttributeError:
                pass
            return response

        return update_wrapper(wrapper, func)

    def get_navigation(self, request, *args, **kwargs):
        user = request.user
        apps = {}
        active = None

        for model, model_admin in self._registry.items():
            label = model._meta.app_label
            perms = model_admin.get_model_perms(request)
            info = (label, model._meta.module_name)
            has_module_perms = user.has_module_perms(label)

            if has_module_perms and perms.get('change', False):
                url = reverse(
                    viewname='admin:%s_%s_changelist' % info,
                    current_app=self.name,
                )

                model = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'url': url,
                    'is_active': request.path.startswith(url),
                }

                if label in apps:
                    apps[label]['models'].append(model)
                else:
                    url = reverse(
                        viewname='admin:app_list',
                        kwargs={'app_label': label},
                        current_app=self.name,
                    )

                    # This is a very naive way to do this, but it should work for now.
                    is_active = request.path.startswith(url)
                    if is_active:
                        active = label

                    apps[label] = {
                        'name': label.title(),
                        'url': url,
                        'is_active': is_active,
                        'models': [model],
                    }

        return {
            'apps': apps,
            'active': active,
        }


site = StratusAdminSite()
