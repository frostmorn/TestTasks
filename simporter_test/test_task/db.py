import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            # don't work with timestamp, lol :D
            # detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        # g.db.row_factory = lambda cursor, row: row[0]

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db( with_inital_data=False):
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    if with_inital_data:
        with current_app.open_resource('inital_data.sql') as f:
            db.executescript(f.read().decode('utf-8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
        Clear existing data and create new tables.
    """
    init_db()
    click.echo('Database initialized.')

@click.command('init-db-with-data')
@with_appcontext
def init_db_with_data_command():
    """
        Clear existing data, creating tables, autoinsert default data from inital_data.sql
    """
    init_db(True)
    click.echo("Database initialized with inital data.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_db_with_data_command)