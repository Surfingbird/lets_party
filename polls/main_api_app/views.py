from aiohttp import web
from polls.main_api_app import auth
import aiohttp
from urllib.parse import urlparse, parse_qsl

from polls.models.model_manager import ModelManager 
from polls.main_api_app.settings import COOKIE_NAME
from polls.models.orm_models import Product, Profile
from polls.main_api_app.elastick_client import ElastickClient

from polls.main_api_app.auth import is_valid
from polls.main_api_app.settings import APP_SECRET

mm = ModelManager()
es_client = ElastickClient()
es_client.connect()

# OK
async def login(request):
    data = {}
    try:
        data = await request.json()
    except ValueError:
        return web.Response(status=web.HTTPBadRequest)

    url = data['url']
    query_params = dict(parse_qsl(urlparse(url).query, keep_blank_values=True))
    ok = is_valid(query=query_params, secret=APP_SECRET)
    if not ok:
       return web.Response(status=web.HTTPForbidden)

    vk_id = int(query_params['vk_user_id'])
    prof = await Profile.objects.get(vk_id=vk_id)
    if prof is None:
        prof = Profile(vk_id=vk_id)
        await prof.save()

    _id = prof['_id']
    payload = {}
    payload['_id'] = _id
    payload['vk_id'] = vk_id

    response = web.Response()
    token = auth.gen_token(payload)
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


# OK
async def product(request):
    product_id = request.match_info['id']

    product = await Product.objects.get(_id=product_id)
    if product is not None:
        product['_id'] = str(product['_id'])

        return web.json_response(product)
    else:
        return web.Response(text="404")  


# OK
async def search_products(request):
    pattern = request.query['pattern']
    data = await es_client.get_products(pattern)

    return web.json_response(data)


async def search_products_result(request):
    pattern = request.query['pattern']
    data = await es_client.get_products_full(pattern)

    return web.json_response(data)


# OK
async def products_list(request):
    start = request.query['start']
    limit = request.query['limit']

    # TODO check valid value
    queryset = Product.objects.filter().offset(start).limit(limit)

    products_page = []

    async for product in queryset:
        product['_id'] = str(product['_id'])
        products_page.append(product)

    total = await Product.objects.count()

    data = {}
    data['total'] = total
    data['products'] = products_page

    return web.json_response(data)

# OK
async def mypage(request):
    uid = request['uid']

    profile = await Profile.objects.get(_id=uid)
    # TODO убрать
    for wish in profile['wishes']:
        wish['product_id'] = str(wish['product_id'])

    # TODO убрать
    for intention in profile['intentions']:
        intention['product_id'] = str(intention['product_id'])
        intention['dest_id'] = str(intention['dest_id'])

    return web.json_response(profile)


# OK
async def my_wishes(request):
    uid = request['uid']

    wishes = await mm.get_users_wishes(uid)
    for wish in wishes:
        wish.pop('sponsor_id')


    return web.json_response(wishes)

# OK
async def add_my_wishe(request):
    uid = request['uid']

    data = {}

    try:
        data = await request.json()
    except ValueError:
        return web.Response(status=web.HTTPBadRequest)

    pid = data['product_id']
    ok = await mm.add_users_wish(uid, pid)
    if ok is not True:
        return web.Response(status=web.HTTPBadRequest)

    return web.Response(status=web.HTTPCreated)

#  OK
async def del_my_wishe(request):
    uid = request['uid']

    data = {}

    try:
        data = await request.json()
    except ValueError:
        return web.Response(status=web.HTTPBadRequest)

    pid = data['product_id']
    ok = await mm.del_users_wish(uid, pid)
    if ok is not True:
        return web.Response(status=web.HTTPBadRequest)
    
    return web.Response()


# OK
async def my_intentions(request):
    uid = request['uid']

    intentions = await mm.get_users_intentions(uid)

    return web.json_response(intentions)


# OK
async def add_my_intentions(request):
    uid = request['uid']

    data = {}

    try:
        data = await request.json()
    except ValueError:
        return web.Response(status=web.HTTPBadRequest)

    pid = data['product_id']
    dest_id = data['dest_id']

    ok = await mm.add_users_intention(uid, pid, dest_id)
    if ok is not True:
        return web.Response(status=web.HTTPBadRequest)

    return web.Response(status=web.HTTPCreated)


# OK
async def del_my_intentions(request):
    uid = request['uid']

    data = {}

    try:
        data = await request.json()
    except ValueError:
        return web.Response(status=web.HTTPBadRequest)

    pid = data['product_id']
    dest_id = data['dest_id']

    ok = await mm.del_users_intention(uid, pid, dest_id)
    if ok is not True:
        return web.Response(status=web.HTTPBadRequest)

    return web.Response(text='del_my_intentions!')


# OK
async def users_wishes(request):
    dest_id = request.match_info['dest_id']
    my_id = request['uid'] 

    wishes = await mm.get_users_wishes(dest_id)
    for wish in wishes:
        sponsor_id = wish.pop('sponsor_id')
        if sponsor_id == my_id:
            wish['reserved_by_me'] = True
        else:
            wish['reserved_by_me'] = False

    return web.json_response(wishes)

# OK
async def intentions_for_user(request):
    dest_id = request.match_info['dest_id']
    uid = request['uid']

    intentions = await mm.intentions_for_user(uid, dest_id)

    return web.json_response(intentions)

async def notifications(request):
    return web.Response(text="notification")

    