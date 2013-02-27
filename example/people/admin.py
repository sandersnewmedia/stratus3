from django.contrib import admin

from stratus.mixins import OrderableMixin

from people.models import Person, Team


class TeamInline(admin.TabularInline):
    model = Team


class PersonAdmin(OrderableMixin, admin.ModelAdmin):
    list_display = ['name', 'hobbies', 'age']
    date_hierarchy = 'birth_date'
    list_filter = ['birth_date']
    inlines = [TeamInline]
    orderable_field = 'age'


admin.site.register(Person, PersonAdmin)
