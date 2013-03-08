import os

from django import forms
from django.core.files.storage import default_storage
from django.db.models.fields.files import ImageFieldFile
from django.forms.util import ErrorList
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _

from stratus.contrib.blocks.models import Block
from stratus.widgets import DisplayableImageInput


class BlockForm(forms.ModelForm):
    storage = default_storage  # This should probably be configurable.

    content_single_line_text = forms.CharField(label=_('Text'), required=False)
    content_multiple_line_text = forms.CharField(label=_('Text'), widget=forms.Textarea, required=False)
    content_html = forms.CharField(label=_('HTML'), widget=forms.Textarea, required=False)
    content_image = forms.ImageField(label=_('Image'), widget=DisplayableImageInput, required=False)

    class Media:
        js = ['blocks/js/block.js']

    class Meta(object):
        model = Block
        fields = ['title', 'slug', 'content_type']

    def __init__(self, *args, **kwargs):
        super(BlockForm, self).__init__(*args, **kwargs)
        content_type = self.initial.get('content_type')
        initial = getattr(self, 'to_initial_%s' % content_type, self.to_initial)()
        self.initial['content_%s' % content_type] = initial

    def to_initial(self):
        return self.instance.content

    def to_initial_image(self):
        # We need to patch in some stuff to make it behave like a image field.
        field = self.instance._meta.get_field_by_name('content')[0]
        field.storage = self.storage
        return ImageFieldFile(self.instance, field, self.instance.content)

    def clean(self):
        content_type = self.cleaned_data['content_type']
        content_field = 'content_%s' % content_type

        if self.cleaned_data.get(content_field) in EMPTY_VALUES:
            message = _('This field is required.')
            self._errors.setdefault(content_field, ErrorList()).append(message)

        return self.cleaned_data

    def save(self, commit=True):
        content_type = self.cleaned_data['content_type']

        getattr(self, 'pre_save_%s' % content_type, self.pre_save)()

        self.instance = super(BlockForm, self).save(commit)

        if commit:
            getattr(self, 'post_save_%s' % content_type, self.post_save)()

        return self.instance

    def pre_save(self):
        self.instance.content = self.cleaned_data['content_%s' % self.cleaned_data['content_type']]

    def pre_save_image(self):
        # No nothing as post_save_image will save the file and update the
        # instance with the correct path.
        pass

    def post_save(self):
        pass

    def post_save_image(self):
        content = self.cleaned_data['content_image']

        base, ext = os.path.splitext(content.name)
        name = os.path.join('blocks', 'images-%s%s' % (self.instance.id, ext))  # This should probably be configurable.

        self.storage.save(name, content)

        self.instance.content = name
        self.instance.save()
