from django.contrib.admin import AdminSite
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.views import password_change
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.template.defaultfilters import slugify
from django.utils.datastructures import SortedDict
from django.utils.functional import update_wrapper
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from stratus import StratusSection


class StratusSite(AdminSite):
    index_template = 'stratus/index.html'
    login_template = 'stratus/login.html'
    logout_template = 'stratus/logout.html'
    password_change_template = 'stratus/password_change.html'
    password_change_done_template = 'stratus/password_change_done.html'

    def __init__(self, name='stratus', app_name='stratus'):
        super(StratusSite, self).__init__(name, app_name)
        self._section_registry = SortedDict()

    def admin_view(self, view, cacheable=False):
        def inner(request, *args, **kwargs):
            if not self.has_permission(request):
                if request.path == reverse('stratus:logout', current_app=self.name):
                    return redirect(reverse('stratus:index', current_app=self.name))
                return self.login(request)
            return view(request, *args, **kwargs)

        if not cacheable:
            inner = never_cache(inner)

        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)

        return update_wrapper(inner, view)

    def check_dependencies(self):
        # No checks needed for now
        pass

    @never_cache
    def index(self, request, extra_context=None):
        # TODO: Add permission checking to only show sections/pages
        # the user is allowed to see.
        context = {
            'title': _('Site administration'),
            'section_list': [{
                'section': section,
                'pages': section.pages(request),
            } for section in self._section_registry.values()],
        }
        context.update(extra_context or {})

        return render(request, self.index_template, context)

    def app_index(self, request, app_label, extra_context=None):
        # TODO: Add permission checking to only show sections/pages
        # the user is allowed to see.
        section = self._section_registry[app_label]

        context = {
            'title': _('{} administration').format(section.name),
            'section_list': [{
                'section': section,
                'pages': section.pages(request),
            }],
        }
        context.update(extra_context or {})

        template = self.app_index_template or [
            'stratus/%s/app_index.html' % app_label,
            'stratus/app_index.html',
        ]

        return render(request, template, context)

    def password_change(self, request):
        url = reverse('stratus:password_change_done', current_app=self.name)

        defaults = {
            'current_app': self.name,
            'post_change_redirect': url,
            'password_change_form': AdminPasswordChangeForm,
            'extra_context': {
                'original': request.user,
            }
        }

        if self.password_change_template is not None:
            defaults['template_name'] = self.password_change_template

        return password_change(request, **defaults)

    def register_section(self, name, namespace=None, admin_section=StratusSection, ordering=None):
        namespace = namespace or slugify(name)
        section = StratusSection(name, namespace, self)

        if ordering is None:
            self._section_registry[namespace] = section
        else:
            self._section_registry.insert(ordering, namespace, section)

        return section


site = StratusSite()
