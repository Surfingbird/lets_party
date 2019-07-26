from aiohttp import web
import auth
import aiohttp

from polls.models.model_manager import ModelManager 
from polls.main_api_app.settings import COOKIE_NAME
from polls.models.orm_models import Product, Profile

mm = ModelManager()

# OK
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

# OK
async def logout(request):
    response = web.Response()
    response.del_cookie(name=COOKIE_NAME)

    return response

# OK
async def new_products(request):
    queryset = Product.objects.filter()
    data = []
    async for doc in queryset:
        doc['_id'] = str(doc['_id'])
        data.append(doc)

    return web.json_response(data)


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

# OK
async def mypage(request):
    uid = request['uid']

    profile = await Profile.objects.get(_id=uid)
    
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


    