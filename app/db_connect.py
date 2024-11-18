import pymysql
import pymysql.cursors
from flask import g

def get_db():
    if 'db' not in g or not is_connection_open(g.db):
        print("Re-establishing closed database connection.")
        g.db = pymysql.connect(
            # Database configuration
            # Configure MySQL
<<<<<<< HEAD
            host = 'jsftj8ez0cevjz8v.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
            user = 'rt5rbja8c5qy738g',
            password = 'nrg2ujozzfcswcl1',
            database = 'l2okyeiy9b6dqfa3',
=======
            host = 'ko86t9azcob3a2f9.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
            user = 'fkwsw1lepapszz6i',
            password = 'snswxulqvzwb0kx2',
            database = 'aqipetggqnho9gww',
>>>>>>> c3681a6c0a71549933b44a1402b765fd210b9af7
            cursorclass=pymysql.cursors.DictCursor  # Set the default cursor class to DictCursor
        )
    return g.db

def is_connection_open(conn):
    try:
        conn.ping(reconnect=True)  # PyMySQL's way to check connection health
        return True
    except:
        return False

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None and not db._closed:
        print("Closing database connection.")
        db.close()