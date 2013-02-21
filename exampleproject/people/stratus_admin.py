import stratus


class PeopleSection(stratus.StratusAppSection):
    pass

people = stratus.site.register(PeopleSection)
