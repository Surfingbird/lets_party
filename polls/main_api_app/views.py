from aiohttp import web
import auth

from polls.models.model_manager import ModelManager 

mm = ModelManager()
DUMMY_USER_ID = "5d2cca26e6f19f24a6a9fd2a"
COOKIE_NAME = "kts_cookie"

# TODO обработка ошибок deocde json 
# TODO не брать каждый раз куки, а просовывать в мидлваре в request


# TODO поддержка JWT
async def login(request):
    data = await request.json()
    response = web.Response()
    response.set_cookie(name=COOKIE_NAME, value=data['id'])

    return response


async def logout(request):
    response = web.Response()
    response.del_cookie(name=COOKIE_NAME)

    return response


# TODO избавиться от костыля с преобразованием ObjectId к строке

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
    cookie = request.cookies[COOKIE_NAME]
    uid = auth.uid_from_cookie(cookie)

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
    cookie = request.cookies[COOKIE_NAME]
    uid = auth.uid_from_cookie(cookie)

    wishes = await mm.get_users_wishes(uid)

    return web.json_response(wishes)


 # TODO валидация JSON
async def add_my_wishe(request):
    cookie = request.cookies[COOKIE_NAME]
    uid = auth.uid_from_cookie(cookie)

    data = await request.json()

    ok = await mm.add_users_wish(uid, data['p_id'])
    if ok is not True:
        return web.Response(status=400)

    return web.Response(status=201)


 # TODO валидация JSON
async def del_my_wishe(request):
    cookie = request.cookies[COOKIE_NAME]
    uid = auth.uid_from_cookie(cookie)

    data = await request.json()

    ok = await mm.del_users_wish(uid, data['p_id'])
    if ok is not True:
        return web.Response(status=400)
    
    return web.Response()


async def my_intentions(request):
    cookie = request.cookies[COOKIE_NAME]
    uid = auth.uid_from_cookie(cookie)

    prof = await mm.get_profile(uid)
    intentions = prof['intentions']
    for intention in intentions:
        intention['p_id'] = str(intention['p_id'])
        intention['dest_id'] = str(intention['dest_id'])

    return web.json_response(intentions)


# TODO валидация JSON
async def add_my_intentions(request):
    cookie = request.cookies[COOKIE_NAME]
    uid = auth.uid_from_cookie(cookie)

    data = await request.json()
    ok = await mm.add_users_intention(uid, data['p_id'], data['dest_id'])
    if ok is not True:
        return web.Response(status=400)

    return web.Response(text='add_my_intentions!')


 # TODO валидация JSON
async def del_my_intentions(request):
    cookie = request.cookies[COOKIE_NAME]
    uid = auth.uid_from_cookie(cookie)

    data = await request.json()
    ok = await mm.del_users_intention(uid, data['p_id'], data['dest_id'])
    if ok is not True:
        return web.Response(status=400)

    return web.Response(text='del_my_intentions!')


# TODO заглушка
async def users_wishes(request):
    nick_or_id = request.match_info['nick_or_id']

    wishes = await mm.get_users_wishes(DUMMY_USER_ID)

    return web.json_response(wishes)


async def intentions_for_user(request):
    return web.Response(text='intentions_for_user!')


    