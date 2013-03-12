from django.contrib import admin

from stratus.blocks.forms import BlockForm
from stratus.blocks.models import BlockPage, Block
from stratus.utils import unchangeable_fields


class BlockMixin(object):
    form = BlockForm

    def get_readonly_fields(self, request, obj=None):
        fields = list(super(BlockMixin, self).get_readonly_fields(request, obj))
        fields += unchangeable_fields(
            user=request.user,
            app_label=self.opts.app_label,
            fields=['title', 'slug', 'content_type'],
        )
        return fields


class BlockInline(BlockMixin, admin.StackedInline):
    model = Block
    extra = 0


class BlockAdmin(BlockMixin, admin.ModelAdmin):
    pass


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
admin.site.register(Block, BlockAdmin)
