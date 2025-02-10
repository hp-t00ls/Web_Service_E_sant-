import mysql.connector

connection_params = {
    "host": "localhost",
    "user": "pascalh_SEV5206E",
    "password": "56167G",
    "database": "pascalh_SEV5206E"
}

def db_connection():
    try:
        conn = mysql.connector.connect(
            host=connection_params['host'],
            user=connection_params['user'],
            password=connection_params['password'],
            database=connection_params['database'],
        )
        output = {
            'CODE': 'DATABASE_CONNECTION_OK',
            'TEXT': "La connexion à la base de données est correcte.",
            'DATA': conn
        }
    except mysql.connector.Error as err:
        output = {
            'CODE': 'FAILED_DATABASE_CONNECTION',
            'TEXT': str(err),
            'DATA': None
        }
        
    return output

def get_cursor(conn):
    return conn.cursor()

def cursor_close(cursor):
    cursor.close()
    
def db_close(conn):
    conn.close()