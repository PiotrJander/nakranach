from django.conf.urls import patterns, include, url

# this would override default django admin site
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.views.decorators.csrf import csrf_exempt

from app import api

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    (r'^api/', include('app.api.urls')),
	(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{
            'document_root': settings.MEDIA_ROOT, 
            'show_indexes': True
        }),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
