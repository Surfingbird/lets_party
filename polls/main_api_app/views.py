from aiohttp import web
from polls.models import product

p_manager = product.ProductManager()

async def index(request):
    return web.Response(text='index!')

async def new_products(request):
    return web.Response(text='new_products!')

async def product(request):
    _id = request.match_info['id']

    product = await p_manager.get_product(_id)
    print(product)

    return web.Response(text='product!')

async def popular_products(request):
    return web.Response(text='popular_products!')

async def search_products(request):
    return web.Response(text='search_products!')

async def get_products(request):
    return web.Response(text='get_products with pattern!')


async def mypage(request):
    return web.Response(text='mypage!')

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


async def users_wishes(request):
    return web.Response(text='users_wishes!')

async def intentions_for_user(request):
    return web.Response(text='intentions_for_user!')


    