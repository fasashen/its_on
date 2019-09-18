import logging

from aiohttp import web

from its_on.settings import get_config
from its_on.db import init_pg, close_pg
from its_on.routes import setup_routes


async def hello_world_handler(request: web.Request) -> web.Response:
    name = request.match_info.get('name', 'Anonymous')
    text = 'Hello, ' + name
    return web.Response(text=text)


async def init_app() -> web.Application:
    app = web.Application()

    app['config'] = get_config()

    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    setup_routes(app)

    # setup_middlewares(app)

    return app


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    app = init_app()

    config = get_config()
    web.run_app(app, host=config['host'], port=config['port'])


if __name__ == '__main__':
    main()
