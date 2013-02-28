from django import forms
from django.template.loader import render_to_string
from django.utils.html import escape


class TemplateWidgetMixn(object):
    template_name = None

    def render(self, name, value, attrs=None):
        context = self.get_context_data(name, value, attrs)
        return render_to_string(self.template_name, context)


class DisplayableImageWidget(TemplateWidgetMixn, forms.ClearableFileInput):
    template_name = 'stratus/widgets/displayable_image_widget.html'

    def __init__(self, max_width=None, max_height=None, *args, **kwargs):
        self.max_width = max_width
        self.max_height = max_height
        super(DisplayableImageWidget, self).__init__(*args, **kwargs)

    def get_context_data(self, name, value, attrs=None):
        file_input = super(forms.ClearableFileInput, self).render(name, value, attrs)

        if not self.is_required:
            clear_name = self.clear_checkbox_name(name)
            clear_id = self.clear_checkbox_id(clear_name)
            clear_input = forms.CheckboxInput().render(clear_name, False, attrs={'id': clear_id})
        else:
            clear_input = None

        return {
            'max_width': self.max_width,
            'max_height': self.max_height,
            'url': value and hasattr(value, 'url') and escape(value.url) or None,
            'file_input': file_input,
            'clear_input': clear_input,
        }
