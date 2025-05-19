import sqlite3 
import functools

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

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("update commited successfully")
            return result
        
        except Exception as e:
            conn.rollback()
            print(f"Data was not saved because a problem was encountered: {e}")
            raise
    return wrapper



@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    #### Update user's email with automatic transaction handling 

update_user_email(user_id=2, new_email='Crawford_Cartwright@hotmail.com')