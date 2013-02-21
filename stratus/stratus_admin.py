from django.contrib.auth.views import login, logout_then_login
from django.utils.translation import ugettext_lazy as _

import stratus


class DashboardPage(stratus.StratusPage):
    template_name = 'stratus/dashboard.html'

    def get(self, request):
        return self.render(request)


class LoginPage(stratus.StratusPage):
    template_name = 'stratus/login.html'
    include_in_nav = False
    login_required = False

    def get(self, request):
        return self.login(request)

    def post(self, request):
        return self.login(request)

    def login(self, request):
        kwargs = {
            'template_name': self.template_name,
            'extra_context': {
                'title': _('Login'),
            }
        }
        kwargs['extra_context'].update(self.get_context_data())
        return login(request, **kwargs)


class LogoutPage(stratus.StratusPage):
    include_in_nav = False

    def get(self, request):
        return logout_then_login(request)

stratus.site.register(DashboardPage)
stratus.site.register(LoginPage)
stratus.site.register(LogoutPage)
