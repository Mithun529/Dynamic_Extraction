# jinka/common/py/database_connection.py
import mysql.connector
from mysql.connector import Error

def get_mysql_connection(db_host: str, db_user: str, db_password: str, db_name: str):
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        if connection.is_connected():
            return connection
        else:
            return None
    except Error as e:
        print(f"Error: {e}")
        return None
