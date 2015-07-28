"""
URLconf for registration and activation, using django-registration's
one-step backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.simple.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize registration behavior, feel free to set up
your own URL patterns for these views instead.

"""

from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from app.accounts.form_helpers import login_form_helper, register_form_helper, password_reset_confirm_form_helper
from app.accounts.views import ProfileRegistrationView, login_with_remember_me, ProfileUpdateView


urlpatterns = patterns('',
                       url(r'^register/$',
                           ProfileRegistrationView.as_view(),
                           name='registration_register'),
                       url(r'^register/closed/$',
                           TemplateView.as_view(template_name='registration/registration_closed.html'),
                           name='registration_disallowed'),
                       url(r'^register/complete/$',
                           TemplateView.as_view(template_name='registration/registration_complete.html'),
                           name='registration_complete'),
                       url(r'^login/$',
                           login_with_remember_me,
                           {'template_name': 'registration/login.html',
                            'extra_context': {'form_helper': login_form_helper}},
                           name='auth_login'),
                       url(r'^logout/$',
                           auth_views.logout,
                           {'template_name': 'registration/logout.html'},
                           name='auth_logout'),
                       url(r'^password/change/$',
                           auth_views.password_change,
                           {'post_change_redirect': reverse_lazy('auth_password_change_done')},
                           name='auth_password_change'),
                       url(r'^password/change/done/$',
                           auth_views.password_change_done,
                           name='auth_password_change_done'),
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           {'post_reset_redirect': reverse_lazy('auth_password_reset_done')},
                           name='auth_password_reset'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           name='auth_password_reset_done'),
                       url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           {'post_reset_redirect': reverse_lazy('auth_password_reset_complete'),
                            'extra_context': {'form_helper': password_reset_confirm_form_helper}},
                           name='auth_password_reset_confirm'),
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='auth_password_reset_complete'),
                       url(r'profile/update/$',
                           ProfileUpdateView.as_view(),
                           name='accounts_profile_update')
                       )
