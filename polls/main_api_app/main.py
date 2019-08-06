import time

from aiohttp import web
from polls.main_api_app.routes import setup_routes
from polls.main_api_app import auth
<<<<<<< HEAD
from polls.models.settings import init_db
=======
from polls.models.db import init_mongodb, DBNAME
from polls.main_api_app.views import init_es_connect
from polls.main_api_app.settings import ES_PATH
>>>>>>> develop

@web.middleware
async def cors_middleware(request, handler):
    response = await handler(request)
  
    return response

<<<<<<< HEAD
def create_app(loop=None):
    init_db(loop=loop)
    app = web.Application(middlewares=[cors_middleware, auth.check_token_middleware])
=======
@web.middleware
async def logger_middleware(request, handler):
    start = time.time()

    response = await handler(request)

    end = time.time()
  
    return response

def create_app(loop=None, dbname=DBNAME, es_path=ES_PATH):
    app = web.Application(middlewares=[auth.check_token_middleware], loop=loop)
>>>>>>> develop
    setup_routes(app)

    init_mongodb(loop=loop, dbname=dbname)
    init_es_connect(loop, path=es_path)

    return app

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)

    app = create_app()

    web.run_app(app)