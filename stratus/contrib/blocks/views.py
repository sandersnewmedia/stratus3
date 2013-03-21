import operator

from django.db import models
from django.views.generic.base import ContextMixin, TemplateView

from stratus.contrib.blocks.models import Block


class BlockMixin(ContextMixin):
    block_keys = []

    def get_block_keys(self):
        return self.block_keys

    def get_blocks(self, *keys):
        keys = [self.get_normalized_key(key) for key in keys]

        blocks = {}
        filters = [self.get_block_filter(group_key, block_keys)
                   for group_key, block_keys in keys]

        if filters:
            for block in Block.objects.filter(reduce(operator.or_, filters)).select_related('group'):
                blocks.setdefault(block.group.key, {})[block.key] = block.render(self.request)

        return blocks

    def get_normalized_key(self, key):
        if isinstance(key, (list, tuple)):
            return key
        return (key, [])

    def get_block_filter(self, group_key, block_keys):
        if block_keys:
            return models.Q(group__key=group_key, key__in=block_keys)
        return models.Q(group__key=group_key)

    def get_context_data(self, **kwargs):
        context = super(BlockMixin, self).get_context_data(**kwargs)

        block_keys = self.get_block_keys()
        blocks = self.get_blocks(*block_keys)
        context['blocks'] = blocks

        return context


class BlockView(BlockMixin, TemplateView):
    pass