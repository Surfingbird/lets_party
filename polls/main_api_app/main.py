from aiohttp import web
from polls.main_api_app.routes import setup_routes
from polls.main_api_app import auth
from polls.models.settings import init_db

@web.middleware
async def cors_middleware(request, handler):
    response = await handler(request)
  
    return response

def create_app(loop=None):
    init_db(loop=loop)
    app = web.Application(middlewares=[cors_middleware, auth.check_token_middleware])
    setup_routes(app)

    return app

if __name__ == "__main__":
    app = create_app()

    web.run_app(app)