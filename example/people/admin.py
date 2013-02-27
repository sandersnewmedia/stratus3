from django.contrib import admin

from people.models import Person, Team


class TeamInline(admin.TabularInline):
    model = Team


class PersonAdmin(admin.ModelAdmin):
    date_hierarchy = 'birth_date'
    list_filter = ['birth_date']
    inlines = [TeamInline]


admin.site.register(Person, PersonAdmin)
