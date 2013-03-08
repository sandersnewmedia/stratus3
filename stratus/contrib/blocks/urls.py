from django.conf.urls import patterns, url


urlpatterns = patterns('stratus.contrib.blocks.views',
    url(r'^(?P<url>.*)/$', 'blockpage', name='stratus_blockpage'),
)
