#!/usr/bin/python3

import mysql.connector

def paginate_users(page_size, offset):
    """
    Retrieves a single page of users from the database.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ALX_prodev",
        consume_results=True
    )

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator function that lazily paginates through all users.
    Only fetches the next page when needed, starting with offset 0.
    """
    offset = 0
    
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        
        yield page
        
        offset += page_size