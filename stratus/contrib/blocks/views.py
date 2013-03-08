from django.views.generic.detail import DetailView

from stratus.contrib.blocks.models import BlockPage


class BlockPageView(DetailView):
    template_name = 'blocks/blockpage.html'
    model = BlockPage
    slug_field = 'url'
    slug_url_kwarg = 'url'


blockpage = BlockPageView.as_view()
