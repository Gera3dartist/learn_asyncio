from views import index, poll, results, vote

from settings import PROJECT_ROOT


def setup_routes(app):
	app.router.add_get('/', index)
	app.router.add_get('/poll/{question_id}', poll, name='poll')
	app.router.add_get('/results/{question_id}/results', results, name='results')
	app.router.add_post('/vote/{question_id}', vote, name='vote')
	setup_static_routes(app)


def setup_static_routes(app):
	app.router.add_static(
		'/static/', 
		path=PROJECT_ROOT / 'static', 
		name='static')
