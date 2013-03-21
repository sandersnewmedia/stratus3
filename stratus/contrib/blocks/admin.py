from django.contrib import admin

from stratus.contrib.blocks.forms import BlockForm
from stratus.contrib.blocks.models import BlockGroup, Block
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
            fields=['key', 'content_type'],
        )
        return fields


class BlockGroupAdmin(admin.ModelAdmin):
    inlines = [BlockInline]
    list_display = ['title', 'key']
    ordering = ['title']

    def get_readonly_fields(self, request, obj=None):
        fields = list(super(BlockGroupAdmin, self).get_readonly_fields(request, obj))
        fields += unchangeable_fields(
            user=request.user,
            app_label=self.opts.app_label,
            fields=['key'],
        )
        return fields


admin.site.register(BlockGroup, BlockGroupAdmin)
