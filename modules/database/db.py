import sqlite3
import os
from flask import g

# DATABASE_LOCATION = ":memory:"
DATABASE_LOCATION = "drawings.sqlite"

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

    print("Database doesn't exist, building schema...")

    SQL_SCHEMA = """CREATE TABLE Drawings (
                        ID integer PRIMARY KEY AUTOINCREMENT,
                        drawing blob,
                        created datetime,
                        location text); """
    db = get()
    db.cursor().executescript(SQL_SCHEMA)
    db.commit()

def query_db(query, args=()):
    # Query the database
    cur = get().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return rv

def store_db(query, args=()):
    # Store entry to database
    cur = get().execute(query, args)        
    get().commit()
    return cur.lastrowid

def close():
    # Close the database (ran automatically by Flask)
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()