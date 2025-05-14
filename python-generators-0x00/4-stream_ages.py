#!/usr/bin/python3

import mysql.connector

def stream_user_ages():
    """
    Generator function that streams user ages one by one from the database.
    Yields only the age field from each user record.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ALX_prodev",
        consume_results=True
    )
    
    cursor = connection.cursor(dictionary=True)

    batch_size = 100
    offset = 0
    
    while True:
        query = "SELECT age FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (batch_size, offset))
        batch = cursor.fetchall()
        
        if not batch:
            break
        
        for user in batch:
            yield user['age']
        
        offset += batch_size
    
    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculates the average age of users without loading the entire dataset
    into memory. Uses the stream_user_ages generator to process ages one by one.
    """
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0
    
    return total_age / count


avg_age = calculate_average_age()
print(f"Average age of users: {avg_age}")