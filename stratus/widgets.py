from django import forms
from django.utils.html import mark_safe


class DisplayableImageInput(forms.ClearableFileInput):

    def render(self, name, value, attrs=None):
        html = super(DisplayableImageInput, self).render(name, value, attrs)
        if value:
            return mark_safe('<img src="%s" style="max-width: 200px; max-height: 200px;"/><br />%s' % (value.url, html))
        return html
