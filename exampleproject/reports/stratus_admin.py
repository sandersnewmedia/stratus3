from django.http import HttpResponse

import stratus


class ReportsSection(stratus.StratusSection):
    pass


class TPSPage(stratus.StratusPage):

    def get(self, request):
        return HttpResponse('TPS Report')


reports = stratus.site.register(ReportsSection)
reports.register(TPSPage)
