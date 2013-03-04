from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from stratus.filters import DateRangeListFilter

from submissions.models import Submission


class SubmissionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_filter = [
        ('created_date', DateRangeListFilter),
        'status',
    ]
    search_fields = ['title']
    actions = ['mark_selected', 'mark_declined', 'mark_revoked']

    def mark_selected(self, request, queryset):
        return queryset.update(status='selected')
    mark_selected.short_description = _('Accept selected submissions')

    def mark_declined(self, request, queryset):
        return queryset.update(status='declined')
    mark_declined.short_description = _('Decline selected submissions')

    def mark_revoked(self, request, queryset):
        return queryset.update(status='revoked')
    mark_revoked.short_description = _('Revoke selected submissions')


admin.site.register(Submission, SubmissionAdmin)
