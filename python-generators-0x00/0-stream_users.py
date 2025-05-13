#!/usr/bin/python3

import mysql.connector
from contextlib import contextmanager

@contextmanager
def connect_to_prodev():
    """Context manager to connect to 'ALX_prodev' database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        yield connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        yield None
    finally:
        if connection and connection.is_connected():
            connection.close()

def stream_users():
    """Generator that streams rows from the 'user_data' table."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ALX_prodev",
        consume_results=True
    )
    
    cursor = connection.cursor(dictionary=True) 
    cursor.execute("SELECT * FROM user_data")
    
    try:
        for row in cursor:
            yield row
    finally:
        cursor.close()
        connection.close()