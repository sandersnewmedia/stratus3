import stratus

from people.models import Person, Team


class TeamInline(stratus.StratusTabularInline):
    model = Team


class PersonAdmin(stratus.StratusModelAdmin):
    date_hierarchy = 'birth_date'
    list_filter = ['birth_date']
    inlines = [TeamInline]


people_section = stratus.site.register_section('People')
people_section.register_model(Person, PersonAdmin)
