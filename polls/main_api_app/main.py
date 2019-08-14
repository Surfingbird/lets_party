import time
import prometheus_client

from aiohttp import web
from polls.main_api_app.routes import setup_routes
from polls.main_api_app import auth
from polls.models.db import init_mongodb, DBNAME, HOST, PORT
from polls.main_api_app.views import init_es_connect
from polls.main_api_app.settings import ES_PATH

RESPONSE_METRIC_NAME = 'request_metric'


@web.middleware
async def cors_middleware(request, handler):
    response = await handler(request)
  
    return response

@web.middleware
async def metric_middleware(request, handler):
    method = request.method
    url = request.path

    response = await handler(request)

    if not (url == '/metrics' or url == '/favicon.ico'):
        request.app[RESPONSE_METRIC_NAME].labels(method=method,
         endpoint=url,
         http_status=response.status).inc()

    return response

def set_up_metrics(app):
    app[RESPONSE_METRIC_NAME] = prometheus_client.Counter(
      RESPONSE_METRIC_NAME, 'Total response count',
      ['method', 'endpoint', 'http_status']
    )

def create_app(loop=None, dbname=DBNAME, es_path=ES_PATH):
    app = web.Application(middlewares=[metric_middleware, auth.check_token_middleware], loop=loop)
    setup_routes(app)

    init_mongodb(loop=loop, dbname=dbname)
    init_es_connect(loop, path=es_path)

    set_up_metrics(app)

    return app

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)

    app = create_app()

    web.run_app(app)