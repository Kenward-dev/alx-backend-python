#!/usr/bin/python3

class DatabaseConnection:
    """A simple context manager for database connections."""
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        print(f"Opening connection to {self.db_name}")
        self.connection = f"Connection to {self.db_name}"
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Closing connection to {self.db_name}")
        self.connection =  None
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return True
    
with DatabaseConnection("my_database") as db:   
    print(f"Using {db.connection}")
    query = "SELECT * FROM users"
    print(f"Executing query: {query}")