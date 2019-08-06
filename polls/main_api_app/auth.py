import jwt
from aiohttp import web

from polls.main_api_app.settings import COOKIE_NAME, MAGIC_WORD, APP_SECRET

login_url = "/auth"

def uid_from_token(token):
    res = ""

    try:
        res = jwt.decode(token, MAGIC_WORD, algorithms=['HS256'])
    except jwt.InvalidSignatureError:
        return None

    return res['_id']


def gen_token(payload):
    return jwt.encode(payload, MAGIC_WORD, algorithm='HS256').decode('utf-8')


@web.middleware
async def check_token_middleware(request, handler):
    url = str(request.rel_url)

    if url == login_url and request.method == "POST":
        pass

    elif COOKIE_NAME in request.cookies:
        token = request.cookies[COOKIE_NAME]
        uid = uid_from_token(token)

        if uid is None:
            return web.Response(status=401)

        request['uid'] = uid

    else:
        return web.Response(status=401)

    response = await handler(request)

    return response


from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlparse, parse_qsl, urlencode
from polls.main_api_app.settings import APP_SECRET

def is_valid(*, query: dict, secret: str) -> bool:
    """Check VK Apps signature"""
    vk_subset = OrderedDict(sorted(x for x in query.items() if x[0][:3] == "vk_"))

    hash_code = b64encode(HMAC(secret.encode(), urlencode(vk_subset, doseq=True).encode(), sha256).digest())
    decoded_hash_code = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')
    return query["sign"] == decoded_hash_code


