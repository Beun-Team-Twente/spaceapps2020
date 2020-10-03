import sqlite3
from flask import g

DATABASE_LOCATION = ":memory:" # In-memory database

def get():
    # Retrieve the Flask database
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE_LOCATION)

    return db

def init_db():
    # Initialize the database if required
    cur = get().execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Drawings';")
    rv = cur.fetchall()
    cur.close()

    if len(rv) > 0:
        return # Database exists


    SQL_SCHEMA = """CREATE TABLE Drawings (
        ID integer PRIMARY KEY AUTOINCREMENT,
        drawing blob,
        created datetime,
        location text);
        """
    db = get()
    db.cursor().executescript(SQL_SCHEMA)
    db.commit()

def query_db(query, args=(), one=False, init = True):
    # Query the database
    try:
        cur = get().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    except sqlite3.OperationalError as e:
        if init:
            print(f"Database probably hasn't been created yet: {e}")
            init_db()
            print("Database initialized; rerunning query")
            return query_db(query, args, one, init = False)

def store_db(query, args=(), init = True):
    # Store entry to database
    try:
        cur = get().execute(query, args)        
        get().commit()
        return cur.lastrowid
    except sqlite3.OperationalError as e:
        if init:
            print(f"Database probably hasn't been created yet: {e}")
            init_db()
            print("Database initialized; rerunning query")
            return store_db(query, args, init = False)

def close():
    # Close the database (ran automatically by Flask)
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()