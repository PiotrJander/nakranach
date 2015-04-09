from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

import base64
import json
import hmac
import hashlib

from .exceptions import FacebookException
from app.pubs.models import Pub

PUB_SESSION_KEY = 'fb_pub'
REDIRECT_SESSION_KEY = 'fb_redirect'

def parse_signed_request(signed_request):
    signature, payload = signed_request.split('.')

    app_secret = settings.FB_APP_SECRET

    digest = hmac.new(app_secret, payload, hashlib.sha256)

    computed_signature = base64.urlsafe_b64encode(digest.digest()).strip('=')
    
    if computed_signature != signature:
        raise FacebookException(_(u'Signature does not match'))

    data = json.loads(base64.urlsafe_b64decode(str(payload)))

    return data

def get_page_ids(request):
    for key, value in request.GET.iteritems():
            if key.startswith('tabs_added'):
                page_id = key[11:][:-1]
                yield page_id

def save_pub_in_session(request, pub_pk, redirect):
    request.session[PUB_SESSION_KEY] = pub_pk
    request.session[REDIRECT_SESSION_KEY] = redirect

def restore_pub_from_session(request):
    try:
        pub_pk = request.session.get(PUB_SESSION_KEY, None)
        redirect = request.session.get(REDIRECT_SESSION_KEY, None)

        if redirect is not None:
            del request.session[REDIRECT_SESSION_KEY]

        if pub_pk is not None:
            del request.session[PUB_SESSION_KEY]
            return Pub.objects.get(pk=pub_pk), redirect
            
    except Pub.DoesNotExist:
        pass

    return None, None