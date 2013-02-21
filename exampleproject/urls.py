from django.conf.urls import patterns, include, url

import stratus


stratus.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(stratus.site.urls)),
)
