from django import forms
from django.utils.safestring import mark_safe


class StratusFileWidget(forms.ClearableFileInput):
    template_with_initial = '<p>%(initial)s %(clear_template)s %(input)s</p>'
    template_with_clear = ('<span class="js-delete"><button class="btn btn-danger" data-toggle="button" '
        'data-on-text="Deleting..." data-off-text="Mark Deleted?">Mark Deleted?</button>'
        '<span style="display: none;">%(clear)s</span></span></p>')

    def get_initial(self, value):
        return '<a class="btn" href="%s">View</a>' % value.url

    def render(self, name, value, attrs=None):
        substitutions = {
            'clear_template': '',
            'input': super(forms.ClearableFileInput, self).render(name, value, attrs),
        }

        template = '%(input)s'

        if value and hasattr(value, 'url'):
            template = self.template_with_initial
            substitutions['initial'] = self.get_initial(value)

            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear'] = forms.CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)


class StratusImageWidget(StratusFileWidget):

    def __init__(self, resize=None, *args, **kwargs):
        self.resize = resize or self.default_resize
        super(StratusImageWidget, self).__init__(*args, **kwargs)

    def default_resize(self, image):
        return image, None, None

    def get_initial(self, value):
        thumbnail, width, height = self.resize(value)
        return (
            '<a href="%(full_url)s">'
            '<img src="%(thumbnail_url)s" %(width)s %(height)s />'
            '</a>' % {
                'full_url': value.url,
                'thumbnail_url': thumbnail.url,
                'width': width and 'width="%s"' % width or '',
                'height': height and 'height="%s"' % height or '',
            }
        )
