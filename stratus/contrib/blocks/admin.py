from django.contrib import admin

from stratus.contrib.blocks.forms import BlockForm
from stratus.contrib.blocks.models import BlockPage, Block


class BlockInline(admin.StackedInline):
    model = Block
    form = BlockForm
    extra = 0


class BlockPageAdmin(admin.ModelAdmin):
    inlines = [BlockInline]


admin.site.register(BlockPage, BlockPageAdmin)
