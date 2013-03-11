from django.contrib import admin

from stratus.contrib.blocks.forms import BlockForm
from stratus.contrib.blocks.models import BlockPage, Block
from stratus.utils import unchangeable_fields


class BlockInline(admin.StackedInline):
    model = Block
    form = BlockForm
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        fields = list(super(BlockInline, self).get_readonly_fields(request, obj))
        fields += unchangeable_fields(
            user=request.user,
            app_label=self.opts.app_label,
            fields=['title', 'slug', 'content_type'],
        )
        return fields


class BlockPageAdmin(admin.ModelAdmin):
    inlines = [BlockInline]

    def get_readonly_fields(self, request, obj=None):
        fields = list(super(BlockPageAdmin, self).get_readonly_fields(request, obj))
        fields += unchangeable_fields(
            user=request.user,
            app_label=self.opts.app_label,
            fields=['url', 'template_name'],
        )
        return fields


admin.site.register(BlockPage, BlockPageAdmin)
