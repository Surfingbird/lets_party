import jwt
from aiohttp import web

from polls.main_api_app.settings import COOKIE_NAME, MAGIC_WORD

login_url = "/auth"

def uid_from_token(token):
    res = ""

    try:
        res = jwt.decode(token, MAGIC_WORD, algorithms=['HS256'])
    except jwt.InvalidSignatureError:
        return None

    return res['id']


def gen_token(uid):
    return jwt.encode({'id': uid}, MAGIC_WORD, algorithm='HS256').decode('utf-8')

@web.middleware
async def check_token_middleware(request, handler):
    url = str(request.rel_url)

    if url == login_url and request.method == "GET":
        pass

    elif COOKIE_NAME in request.cookies:
        token = request.cookies[COOKIE_NAME]
        uid = uid_from_token(token)

        request['uid'] = uid

        if uid is None:
            return web.HTTPUnauthorized

    else:
        return web.Response(status=401)


    response = await handler(request)

    return response