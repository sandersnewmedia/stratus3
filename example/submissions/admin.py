from django.contrib import admin

from stratus.filters import DateRangeListFilter, DropdownListFilter, SearchListFilter

from submissions.models import Submission, SubmissionEstimate


class SubmissionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_filter = [
        ('created_date', DateRangeListFilter),
        ('title', SearchListFilter),
        ('status', DropdownListFilter),
    ]
    search_fields = ['title']


class SubmissionEstimateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Submission, SubmissionAdmin)
admin.site.register(SubmissionEstimate, SubmissionEstimateAdmin)
