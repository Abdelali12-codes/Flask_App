
import sqlite3


from flask import current_app , g
from flask.cli import with_appcontext



def get_db():

    if 'db' not in g :
        g.db = sqlite3.connect("employee.db")
        g.db.row_factory = sqlite3.Row

    return g.db



def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()