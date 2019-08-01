from aiohttp import web
from polls.main_api_app.routes import setup_routes
from polls.main_api_app import auth
from polls.models.db import init_mongodb, DBNAME

@web.middleware
async def cors_middleware(request, handler):
    response = await handler(request)
  
    return response

def create_app(loop=None, dbname=DBNAME):
    app = web.Application(middlewares=[cors_middleware, auth.check_token_middleware], loop=loop)
    setup_routes(app)

    init_mongodb(loop=loop, dbname=dbname)

    return app

if __name__ == "__main__":
    app = create_app()

    web.run_app(app)