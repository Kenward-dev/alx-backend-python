#!/usr/bin/python3

class ExecuteQuery:
    """A simple context manager for executing parameterized queries."""
    def __init__(self, db_name, query, age):
        self.db_name = db_name
        self.connection = None
        self.query = query
        self.age = age
        self.result = None

    def __enter__(self):
        print(f"Opening connection to {self.db_name}")
        self.connection = f"Connection to {self.db_name}"

        print(f"Executing query: {self.query} with age: {self.age}")
        self.result = f"Result of query '{self.query}' with age parameter {self.age}"
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Query execution completed")
        self.result = None
        print(f"Closing connection to {self.db_name}")
        self.connection =  None
        
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return True  

with ExecuteQuery("SELECT * FROM users WHERE age > ?", 25) as query:
    print(f"Using result: {query.result}")