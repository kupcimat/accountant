import logging

from aiohttp import web

from accountant import config
from accountant.worker import routes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s",
)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes.create_routes())

    web.run_app(app, port=config.PORT)
