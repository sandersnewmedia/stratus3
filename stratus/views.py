from django.views.generic.base import View


class StratusPageMixin(object):
    page = None


class StratusPageView(StratusPageMixin, View):

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right page method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self.page, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        self.request = request
        return handler(request, *args, **kwargs)
