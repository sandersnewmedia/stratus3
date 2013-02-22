from django.contrib import admin


class StratusModelAdmin(admin.ModelAdmin):
    delete_selected_confirmation_template = 'stratus/delete_selected_confirmation.html'

    def __init__(self, model, admin_site, page):
        self.page = page
        super(StratusModelAdmin, self).__init__(model, admin_site)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        opts = self.model._meta
        app_label = opts.app_label

        self.add_form_template = self.change_form_template = (
            'stratus/{}/{}/change_form.html'.format(app_label, opts.object_name.lower()),
            'stratus/{}/change_form.html'.format(app_label),
            'stratus/change_form.html',
        )

        extra_context = self.page.get_context_data(request)
        context.update(extra_context)
        return super(StratusModelAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    def changelist_view(self, request, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label

        self.change_list_template = (
            'stratus/{}/{}/change_list.html'.format(app_label, opts.object_name.lower()),
            'stratus/{}/change_list.html'.format(app_label),
            'stratus/change_list.html'
        )

        context = extra_context or {}
        context.update(self.page.get_context_data(request))
        return super(StratusModelAdmin, self).changelist_view(request, context)

    def delete_view(self, request, object_id, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label

        self.delete_confirmation_template = (
            'stratus/{}/{}/delete_confirmation.html'.format(app_label, opts.object_name.lower()),
            'stratus/{}/delete_confirmation.html'.format(app_label),
            'stratus/delete_confirmation.html'
        )

        context = extra_context or {}
        context.update(self.page.get_context_data(request))
        return super(StratusModelAdmin, self).delete_view(request, object_id, context)

    def history_view(self, request, object_id, extra_context=None):
        opts = self.model._meta
        app_label = opts.app_label

        self.object_history_template = (
            'stratus/{}/{}/object_history.html'.format(app_label, opts.object_name.lower()),
            'stratus/{}/object_history.html'.format(app_label),
            'stratus/object_history.html'
        )

        context = extra_context or {}
        context.update(self.page.get_context_data(request))
        return super(StratusModelAdmin, self).history_view(request, object_id, context)
