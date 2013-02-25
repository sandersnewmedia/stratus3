from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict

from stratus import StratusModelAdmin


class StratusSection(object):

    def __init__(self, name, namespace, admin_site):
        self.name = name
        self.namespace = namespace
        self.admin_site = admin_site
        self._registry = SortedDict()

    def register(self, namespace, admin, ordering=None):
        if ordering is None:
            self._registry[namespace] = admin
        else:
            self._registry.insert(ordering, namespace, admin)

    def unregister(self, namespace):
        del self._registry[namespace]

    def register_model(self, model, model_admin=StratusModelAdmin, ordering=None):
        namespace = '{}/{}'.format(model._meta.app_label, model._meta.module_name)
        self.admin_site.register(model, model_admin)
        admin = self.admin_site._registry[model]
        self.register(namespace, admin, ordering)

    def unregister_model(self, model):
        namespace = '{}/{}'.format(model._meta.app_label, model._meta.module_name)
        self.admin_site.unregister(model)
        self.unregister(namespace)

    def url(self):
        return reverse('stratus:app_list', kwargs={'app_label': self.namespace}, current_app=self.name)

    def pages(self, request):
        # TODO: Add permission checks to only include pages the user
        # is allowed to see.
        return self._registry.values()
