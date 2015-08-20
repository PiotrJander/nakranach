from django.conf.urls import patterns, include, url

# this would override default django admin site
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


admin.autodiscover()
urlpatterns = patterns('',
    (r'^oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    (r'^api/', include('app.api.urls')),
	(r'^admin/', include(admin.site.urls)),
    (r'^fb/', include('app.fb.urls')),
    (r'^users/', include('app.users.urls', namespace='user')),
    (r'^accounts/', include('app.accounts.urls')),
    (r'^taps/', include('app.taps.urls', namespace='tap')),
    (r'^pub/beers/', include('app.pubs.urls',namespace='pub')),
    (r'^beers/', include('app.beers.urls', namespace='beers')),
    (r'^', include('app.main.urls', namespace='main')),
)


if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{
            'document_root': settings.MEDIA_ROOT, 
            'show_indexes': True
        }),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
