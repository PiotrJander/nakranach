# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

register = template.Library()

FACEBOOK_DIALOG_ADD_URL = u'http://www.facebook.com/dialog/pagetab?app_id=%s&display=popup&next=%s'

@register.simple_tag
def add_tab_url():
    return FACEBOOK_DIALOG_ADD_URL % (settings.FB_APP_ID, 'https://balrog.makimo.pl/fb/')