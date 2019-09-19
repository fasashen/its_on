import logging

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec

from its_on.settings import get_config
from its_on.db import init_pg, close_pg
from its_on.middlewares import setup_middlewares
from its_on.routes import setup_routes


async def init_app() -> web.Application:
    app = web.Application()

    app['config'] = get_config()

    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    setup_routes(app)
    setup_aiohttp_apispec(app=app, request_data_name='validated_data')
    setup_middlewares(app)

    return app


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    app = init_app()
    config = get_config()
    web.run_app(app, host=config['host'], port=config['port'])


if __name__ == '__main__':
    main()
