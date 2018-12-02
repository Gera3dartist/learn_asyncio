import logging
import sys

from aiohttp import web
import aiohttp_jinja2
import jinja2
import aiohttp_debugtoolbar
from aiohttp_debugtoolbar import toolbar_middleware_factory

from router import setup_routes
from settings import get_config, TEMPLATES
from db import init_pg, clean_pg
from middlewares import setup_middlewares


def init_app(argv=None):
	app = web.Application()

	aiohttp_debugtoolbar.setup(app)

	# ----- setup an applicatin ----- #
	setup_routes(app)
	app['config'] = get_config()

	# setup jinja2 templates
	aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader([TEMPLATES]))

	# ----- setup middleware ----- #
	setup_middlewares(app)

	# ----- init app on signal ----- #
	app.on_startup.append(init_pg)
	app.on_cleanup.append(clean_pg)

	return app


def main(argv):
	logging.basicConfig(level=logging.DEBUG)
	app = init_app()
	config = get_config()
	web.run_app(app, host=config['host'], port=config['port'])


if __name__ == '__main__':
	main(sys.argv[1:])

