from django.contrib.admin import filters
from django.db import models


class StratusListFilter(filters.ListFilter):
    template = 'stratus/filter.html'


class StratusSimpleListFilter(filters.ListFilter):
    template = 'stratus/filter.html'


class StratusFieldListFilter(filters.FieldListFilter):
    template = 'stratus/filter.html'


class StratusRelatedFieldListFilter(filters.RelatedFieldListFilter):
    template = 'stratus/filter.html'


class StratusBooleanFieldListFilter(filters.BooleanFieldListFilter):
    template = 'stratus/filter.html'


class StratusChoicesFieldListFilter(filters.ChoicesFieldListFilter):
    template = 'stratus/filter.html'


class StratusDateFieldListFilter(filters.DateFieldListFilter):
    template = 'stratus/filter.html'


class StratusAllValuesFieldListFilter(filters.AllValuesFieldListFilter):
    template = 'stratus/filter.html'


filters.FieldListFilter.register(
    test=lambda f: hasattr(f, 'rel') and bool(f.rel) or isinstance(f, models.related.RelatedObject),
    list_filter_class=StratusRelatedFieldListFilter,
    take_priority=True,
)

filters.FieldListFilter.register(
    test=lambda f: isinstance(f, (models.BooleanField, models.NullBooleanField)),
    list_filter_class=StratusBooleanFieldListFilter,
    take_priority=True,
)

filters.FieldListFilter.register(
    test=lambda f: bool(f.choices),
    list_filter_class=StratusChoicesFieldListFilter,
    take_priority=True,
)

filters.FieldListFilter.register(
    test=lambda f: isinstance(f, models.DateField),
    list_filter_class=StratusDateFieldListFilter,
    take_priority=True,
)

filters.FieldListFilter.register(
    test=lambda f: True,
    list_filter_class=StratusAllValuesFieldListFilter,
    take_priority=True,
)
