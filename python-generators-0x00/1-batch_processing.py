#!/usr/bin/python3

import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that streams rows from the 'user_data' table in batches."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ALX_prodev",
        consume_results=True
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data WHERE age > 25")
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Function to process user data in batches."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            return user


