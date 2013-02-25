from stratus.options import (
    StratusModelAdmin,
    StratusStackedInline,
    StratusTabularInline,
)
from stratus.sections import StratusSection
from stratus.sites import site
from stratus.filters import (
    StratusListFilter,
    StratusSimpleListFilter,
    StratusFieldListFilter,
    StratusBooleanFieldListFilter,
    StratusRelatedFieldListFilter,
    StratusChoicesFieldListFilter,
    StratusDateFieldListFilter,
    StratusAllValuesFieldListFilter,
)


def autodiscover():
    """
    Auto-discover INSTALLED_APPS stratus_admin.py modules and fail silently
    when not present. This forces and import on them to register any stratus
    bits they may want.

    """
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attemp to import the app's stratus module.
        try:
            before_import_registry = copy.copy(site._registry)
            import_module('{}.stratus_admin'.format(app))
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions.
            site._registry = before_import_registry

            # Decide whether to bubble up this error. If the app just
            # doesn't have an admin module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'stratus_admin'):
                raise
