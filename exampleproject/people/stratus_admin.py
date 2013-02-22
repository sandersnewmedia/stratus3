from django.contrib import admin

import stratus

from people.models import Person, Team


class PeopleSection(stratus.StratusSection):
    pass


class TeamInline(admin.TabularInline):
    model = Team


class PersonModelAdmin(stratus.StratusModelAdmin):
    save_on_top = True
    readonly_fields = ['name']
    inlines = [TeamInline]


class PersonPage(stratus.StratusModelAdminPage):
    model = Person
    admin_class = PersonModelAdmin


people = stratus.site.register(PeopleSection)
people.register(PersonPage)
