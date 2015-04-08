import base64
import json

def parse_signed_request(signed_request):
    signature, payload = signed_request.split('.')

    print signature

    data = json.loads(base64.b64decode(payload))
    return data