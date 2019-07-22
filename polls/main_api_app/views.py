from aiohttp import web
import auth
import aiohttp

from polls.models.model_manager import ModelManager 

mm = ModelManager()
COOKIE_NAME = "kts_cookie"

# TODO избавиться от костыля с преобразованием ObjectId к строке

async def subscription(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # while True:
    #     await ws.ping()


    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.ping()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

async def login(request):
    data = {}

    try:
        data = await request.json()
    except ValueError:
        return web.Response(status=400)

    _id = data['id']
    ok = mm.check_user(_id)
    if not ok:
        return web.Response(status=404)

    response = web.Response()
    token = auth.gen_token(data['id'])
    response.set_cookie(name=COOKIE_NAME, value=token)

    return response


async def logout(request):
    response = web.Response()
    response.del_cookie(name=COOKIE_NAME)

    return response


async def new_products(request):
    products = await mm.get_products()
    for product in products:
        product['_id'] = str(product['_id'])

    return web.json_response(products)


async def product(request):
    _id = request.match_info['id']
    product = await mm.get_product(_id)
    if product is not None:
        product['_id'] = str(product['_id'])

        return web.json_response(product)
    else:
        return web.Response(text="404")  


# TODO опциональная ручка
async def popular_products(request):
    return web.Response(text='popular_products!')

# TODO
async def search_products(request):
    return web.Response(text='search_products!')

# TODO
async def get_products(request):
    return web.Response(text='get_products with pattern!')


async def mypage(request):
    uid = request['uid']

    profile = await mm.get_profile(uid)
    profile['_id'] = str(profile['_id'])
    for wish in profile['wishes']:
        wish['p_id'] = str(wish['p_id'])
        wish.pop('sponsor_id', None)

    for intention in profile['intentions']:
        intention['p_id'] = str(intention['p_id'])
        intention['dest_id'] = str(intention['dest_id'])
    
    return web.json_response(profile)


async def my_wishes(request):
    uid = request['uid']

    wishes = await mm.get_users_wishes(uid)

    return web.json_response(wishes)


async def add_my_wishe(request):
    uid = request['uid']

    data = {}

    try:
        data = await request.json()
    except ValueError:
        return web.Response(status=400)

    ok = await mm.add_users_wish(uid, data['p_id'])
    if ok is not True:
        return web.Response(status=400)

    return web.Response(status=201)


async def del_my_wishe(request):
    uid = request['uid']

    data = {}

    try:
        data = await request.json()
    except ValueError:
        return web.Response(status=400)

    ok = await mm.del_users_wish(uid, data['p_id'])
    if ok is not True:
        return web.Response(status=400)
    
    return web.Response()


async def my_intentions(request):
    uid = request['uid']

    intentions = await mm.get_users_intentions(uid)

    return web.json_response(intentions)

async def add_my_intentions(request):
    uid = request['uid']

    data = {}

    try:
        data = await request.json()
    except ValueError:
        return web.Response(status=400)

    ok = await mm.add_users_intention(uid, data['p_id'], data['dest_id'])
    if ok is not True:
        return web.Response(status=400)

    return web.Response(text='add_my_intentions!')


async def del_my_intentions(request):
    uid = request['uid']

    data = {}

    try:
        data = await request.json()
    except ValueError:
        return web.Response(status=400)


    ok = await mm.del_users_intention(uid, data['p_id'], data['dest_id'])
    if ok is not True:
        return web.Response(status=400)

    return web.Response(text='del_my_intentions!')


async def users_wishes(request):
    dest_id = request.match_info['dest_id']

    wishes = await mm.get_users_wishes(dest_id)

    return web.json_response(wishes)


async def intentions_for_user(request):
    dest_id = request.match_info['dest_id']
    uid = request['uid']

    intentions = await mm.intentions_for_user(uid, dest_id)

    return web.json_response(intentions)


    