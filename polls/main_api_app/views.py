from aiohttp import web

from polls.models.model_manager import ModelManager 

mm = ModelManager()
DUMMY_USER_ID = "5d2cca26e6f19f24a6a9fd2a"

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


async def search_products(request):
    return web.Response(text='search_products!')


async def get_products(request):
    return web.Response(text='get_products with pattern!')


async def mypage(request):
    return web.Response(text='mypage!')

# TODO заглушка на id пользователя
async def my_wishes(request):
    return web.Response(text='my_wishes!')


async def add_my_wishe(request):
    return web.Response(text='add_my_wishe!')


async def del_my_wishe(request):
    return web.Response(text='del_my_wishe!')


async def my_intentions(request):
    return web.Response(text='my_intentions!')


async def add_my_intentions(request):
    return web.Response(text='add_my_intentions!')


async def del_my_intentions(request):
    return web.Response(text='del_my_intentions!')

# TODO заглушка
async def users_wishes(request):
    nick_or_id = request.match_info['nick_or_id']

    wishes = await mm.get_users_wishes(DUMMY_USER_ID)

    return web.json_response(wishes)


async def intentions_for_user(request):
    return web.Response(text='intentions_for_user!')


    