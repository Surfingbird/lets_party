from aiohttp import web
from routes import setup_routes
from settings import config

if __name__ == "__main__":
    app = web.Application()
    setup_routes(app)
    app['config'] = config

    web.run_app(app)