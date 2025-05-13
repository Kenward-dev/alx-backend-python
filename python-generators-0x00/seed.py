#!/usr/bin/python3

import uuid
import csv
from contextlib import contextmanager

import mysql.connector


@contextmanager
def cursor_context(connection):
    """Context manager for database cursors"""
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def connect_db():
    """Connects to the MySQL database server"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None


def create_database(connection):
    """Creates the database ALX_prodev if it does not exist"""
    try:
        with cursor_context(connection) as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")


def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to 'ALX_prodev' database: {err}")
        return None


def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields"""
    try:
        with cursor_context(connection) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    user_id CHAR(36) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    age DECIMAL(5,2) NOT NULL,
                    INDEX (user_id)
                )
            """)
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


def read_csv_generator(filename):
    """Generator function to read data from CSV file"""
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                yield row
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error reading CSV file: {e}")


def insert_data(connection, csv_file):
    """Inserts data in the database if it does not exist"""
    try:
        with cursor_context(connection) as cursor:
            # Check existing user IDs to avoid duplicates
            cursor.execute("SELECT user_id FROM user_data")
            existing_ids = set(row[0] for row in cursor.fetchall())
            
            insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """
            
            for row in read_csv_generator(csv_file):
                if len(row) >= 3:  # Ensure we have at least name, email, and age
                    user_id = str(uuid.uuid4())
                    name = row[0]
                    email = row[1]
                    age = float(row[2])
                    
                    if user_id not in existing_ids:
                        cursor.execute(insert_query, (user_id, name, email, age))
                        existing_ids.add(user_id)
            
            connection.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except Exception as e:
        print(f"Error processing data: {e}")