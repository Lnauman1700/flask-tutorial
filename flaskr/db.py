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

# g is a special object that's unique for each request, used to store data
# that might be accessed by multiple functions during the request
