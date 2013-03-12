from django.conf.urls import patterns, url


urlpatterns = patterns('stratus.blocks.views',
    url(r'^$', 'blockpage', {'url': '/'}, name='stratus_blockpage'),
    url(r'^(?P<url>.*)/$', 'blockpage', name='stratus_blockpage'),
)
