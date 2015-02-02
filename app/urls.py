from django.conf.urls import patterns, include, url

# this would override default django admin site
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.views.decorators.csrf import csrf_exempt

admin.autodiscover()

urlpatterns = patterns('',
)

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{
            'document_root': settings.MEDIA_ROOT, 
            'show_indexes': True
        }),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
