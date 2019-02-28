import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        # establishes a connection to the file pointed at by the 'DATABASE' key (config.py in this case)
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        # return rows that behave like dicts
        g.db.row_factory = sqlite3.Row

    return g.db

# checks for a connection, then closes it if it exists
def close_db(e = None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    # opens a file (schema.sql), and reads it later
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# init-db is a command line command, which calls the init_db function and shows a success messsage
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    # tells flask to call the close_db function when cleaning up after returning the response
    app.teardown_appcontext(close_db)
    # adds a command that can be called w/ the flask command (init_db_command)
    app.cli.add_command(init_db_command)

# g is a special object that's unique for each request, used to store data
# that might be accessed by multiple functions during the request
