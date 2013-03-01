from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

import stratus


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(stratus.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
