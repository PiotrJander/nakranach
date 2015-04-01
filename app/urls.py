from django.conf.urls import patterns, include, url

# this would override default django admin site
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, DetailView

from django.views.decorators.csrf import csrf_exempt

from app.pubs.models import Pub

from app import api

admin.autodiscover()

urlpatterns = patterns('',
    (r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    (r'^api/', include('app.api.urls')),
	(r'^admin/', include(admin.site.urls)),
    (r'^fb/', include('app.fb.urls')),
    (r'', include('app.main.urls'))
)

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{
            'document_root': settings.MEDIA_ROOT, 
            'show_indexes': True
        }),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
