import stratus

from people.models import Person, Team


stratus.site.register(Person, list_display=['name', 'order'], search_fields=['name'], date_hierarchy='birthdate', list_filter=['name'], list_editable=['order'])
stratus.site.register(Team)
