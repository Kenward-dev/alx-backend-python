#!/usr/bin/python3

import mysql.connector

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