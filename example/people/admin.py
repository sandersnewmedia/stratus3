import stratus

from people.models import Person, Team


stratus.site.register(Person, list_display=['name', 'order'], fields=(('name', 'order'),))
stratus.site.register(Team)
