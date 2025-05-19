import sqlite3 
import functools


query_cache = {}

def with_db_connection(func):
    """Decorator function that opens a database connection, passes it to the function and closes it afterword"""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        
        try:
            return func(conn, *args, **kwargs)
        
        finally:
            conn.close()
    
    return wrapper

def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string.
    Return cached result if the query is in the cache.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query')
        
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]
        
        result = func(conn, *args, **kwargs)
        
        query_cache[query] = result
        print(f"Cached result for query: {query}")
        
        return result
    
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")