from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

import base64
import json
import hmac
import hashlib

from .exceptions import FacebookException

def parse_signed_request(signed_request):
    signature, payload = signed_request.split('.')

    app_secret = settings.FB_APP_SECRET

    digest = hmac.new(app_secret, payload, hashlib.sha256)

    computed_signature = base64.urlsafe_b64encode(digest.digest()).strip('=')
    
    if computed_signature != signature:
        raise FacebookException(_(u'Signature does not match'))

    data = json.loads(base64.urlsafe_b64decode(str(payload)))
    return data