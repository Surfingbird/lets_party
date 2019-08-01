from aiohttp import web
from polls.main_api_app.routes import setup_routes
from polls.main_api_app import auth
from polls.models.db import init_mongodb, DBNAME
from polls.main_api_app.views import init_es_connect
from polls.main_api_app.settings import ES_PATH

@web.middleware
async def cors_middleware(request, handler):
    response = await handler(request)
  
    return response

def create_app(loop=None, dbname=DBNAME, es_path=ES_PATH):
    app = web.Application(middlewares=[auth.check_token_middleware], loop=loop)
    setup_routes(app)

    init_mongodb(loop=loop, dbname=dbname)
    init_es_connect(loop, path=ES_PATH)

    return app

if __name__ == "__main__":
    app = create_app()

    web.run_app(app)