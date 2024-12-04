# jinka/common/py/database_service.py
import csv
from datetime import datetime
from common.py.database_connection import get_mysql_connection


def fetch_data_from_mysql(db_host: str, db_user: str, db_password: str, db_name: str, table_name: str):
    connection = get_mysql_connection(db_host, db_user, db_password, db_name)

    if connection is None:
        return {"error": "Database connection failed"}

    try:
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for named columns
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)

        rows = cursor.fetchall()

        if rows:
            return {"data": rows}
        else:
            return {"error": "No data found"}
    except mysql.connector.Error as e:
        return {"error": f"Error executing query: {e}"}
    finally:
        connection.close()

def save_table_data_to_csv(headers, data, csv_filename="table_data_output.csv"):
    """
    Saves table data to a CSV file.
    """
    if not csv_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"table_data_{timestamp}.csv"

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

    return csv_filename
