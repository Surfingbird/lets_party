import random

from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode
from polls.main_api_app.settings import APP_SECRET

def get_vk_hashcode(payload, secret):
    vk_subset = OrderedDict(sorted(x for x in payload.items() if x[0][:3] == "vk_"))
    hash_code = b64encode(HMAC(secret.encode(), urlencode(vk_subset, doseq=True).encode(), sha256).digest())
    decoded_hash_code = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')

    return decoded_hash_code

def gen_vk_url(vk_id, secret):
    path = 'http://127.0.0.1:9001/?' 

    payload = dict()
    payload['vk_access_token_settings'] = 'friends'
    payload['vk_app_id'] = 7061026
    payload['vk_are_notifications_enabled'] = 0
    payload['vk_is_app_user'] = 1
    payload['vk_language'] = 'ru'
    payload['vk_platform'] = 'desktop_web'
    payload['vk_ref'] = 'other'

    payload['vk_user_id'] = vk_id

    sign = get_vk_hashcode(payload, secret)
    payload['sign'] = sign

    qstr = urlencode(payload)

    url = path + qstr

    return url