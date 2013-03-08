from django import forms
from django.utils.translation import ugettext_lazy as _

from stratus.contrib.blocks.models import Block


class BlockForm(forms.ModelForm):
    content_single_line_text = forms.CharField(label=_('Text'), required=False)
    content_multiple_line_text = forms.CharField(label=_('Text'), widget=forms.Textarea, required=False)
    content_html = forms.CharField(label=_('HTML'), widget=forms.Textarea, required=False)

    class Media:
        js = ['blocks/js/block.js']

    class Meta(object):
        model = Block
        fields = ['title', 'slug', 'content_type']

    def __init__(self, *args, **kwargs):
        super(BlockForm, self).__init__(*args, **kwargs)
        content_type = self.initial.get('content_type')
        self.initial['content_%s' % content_type] = self.instance.content
