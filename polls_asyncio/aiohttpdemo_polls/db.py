from sqlalchemy import (MetaData, Table, Column, ForeignKey, Integer, String, Date)
from aiopg.sa import create_engine


meta = MetaData()


question = Table(
	'question', meta,
	Column('id', Integer, primary_key=True),
	Column('question_text', String(200), nullable=False),
	Column('pub_date', Date, nullable=False),
)

choice = Table(
	'choice', meta,
	Column('id', Integer, primary_key=True),
	Column('choice_text', String(200), nullable=False),
	Column('votes', Integer, server_default="0", nullable=False),
	Column('question_id', Integer, ForeignKey('question.id', ondelete='CASCADE')),
)


class RecordNotFound(Exception):
	"""Requested record in database was not found"""


async def init_pg(app):
	conf = app['config']['postgres']
	engine = await create_engine(
		database=conf['database'],
		user=conf['user'],
		password=conf['password'],
		host=conf['host'],
		port=conf['port'],
		minsize=conf['minsize'],
		maxsize=conf['maxsize']
	)
	app['db'] = engine


async def clean_pg(app):
	app['db'].close()
	await app['db'].wait_closed()


async def get_question(conn, question_id):
	result = await conn.execute(question.select().where(question.c.id == question_id))
	question_record = await result.first()
	if not question_record:
		msg = f'Qustion with id: {question_id} does not exists'
		raise RecordNotFound(msg)
	result = await conn.execute(
		choice.select()
		.where(choice.c.question_id == question_id)
		.order_by(choice.c.id))
	choice_records = await result.fetchall()
	return question_record, choice_records


async def vote(conn, question_id, choice_id):
	result = await conn.execute(
		choice.update()
		.returning(*choice.c)
		.where(choice.c.question_id == question_id)
		.where(choice.c.id == choice_id)
		.values(votes=choice.c.votes+1))
	record = await result.fetchone()
	if not record:
		msg = f"Question with id: {question_id} and choice id: {choice_id} does not exists"
		raise RecordNotFound(msg)

