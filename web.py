import logging

from aiohttp import web

from accountant.web import config, routes

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes.create_routes())

    web.run_app(app, port=config.PORT)