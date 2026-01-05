import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

def create_table(connection, table_name, create_table_query):
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{table_name}' created successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


conn = create_connection("mydb", "postgres", "123", "localhost", "5432")

# if conn:
#     cur = conn.cursor()
#     cur.execute("SELECT current_database(), current_user;")
#     print(cur.fetchone())
#     cur.close()
#     conn.close()

# if conn:
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM users;")
#     rows = cur.fetchall()

#     for row in rows:
#         print(row)

#     cur.close()
#     conn.close()

