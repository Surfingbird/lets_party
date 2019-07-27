from aiohttp import web
from routes import setup_routes
import auth

@web.middleware
async def cors_middleware(request, handler):
    response = await handler(request)
  
    return response


if __name__ == "__main__":
    # app = web.Application(middlewares=[cors_middleware, auth.check_token_middleware])
    app = web.Application()
    setup_routes(app)

    web.run_app(app)