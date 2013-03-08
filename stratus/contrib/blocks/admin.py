from django.contrib import admin

from stratus.contrib.blocks.forms import BlockForm
from stratus.contrib.blocks.models import BlockPage, Block


class BlockInline(admin.StackedInline):
    model = Block
    form = BlockForm
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        fields = super(BlockInline, self).get_readonly_fields(request, obj)

        if not request.user.has_perm('%s.change_title' % self.opts.app_label):
            fields += ('title',)

        if not request.user.has_perm('%s.change_slug' % self.opts.app_label):
            fields += ('slug',)

        if not request.user.has_perm('%s.change_content_type' % self.opts.app_label):
            fields += ('content_type',)

        return fields


class BlockPageAdmin(admin.ModelAdmin):
    inlines = [BlockInline]

    def get_readonly_fields(self, request, obj=None):
        fields = super(BlockPageAdmin, self).get_readonly_fields(request, obj)

        if not request.user.has_perm('%s.change_url' % self.opts.app_label):
            fields += ('url',)

        if not request.user.has_perm('%s.change_template_name' % self.opts.app_label):
            fields += ('template_name',)

        return fields


admin.site.register(BlockPage, BlockPageAdmin)
