# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

register = template.Library()

FACEBOOK_DIALOG_ADD_URL = u'http://www.facebook.com/dialog/pagetab?app_id=%s&display=popup&next=%s'

@register.simple_tag
def add_tab_url():
    current_site = Site.objects.get_current()

    next_url = 'https://%s%s' % (current_site.domain, reverse('fb-taps'))

    return FACEBOOK_DIALOG_ADD_URL % (settings.FB_APP_ID, next_url)