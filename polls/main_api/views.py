from aiohttp import web

async def index(request):
    return web.Response(text='index!')

async def near_events(request):
    return web.Response(text='near_events!')

async def event(request):
    return web.Response(text='event!')

async def popular_events(request):
    return web.Response(text='popular_events!')

async def search_events(request):
    return web.Response(text='search_events!')

async def get_events(request):
    return web.Response(text='get_events with pattern!')


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


    