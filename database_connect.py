import psycopg2
from psycopg2 import OperationalError

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS production_data (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    station_name TEXT,
    model_type TEXT,
    ok_quantity INTEGER,
    ng_quantity INTEGER,
    production_time INTERVAL,
    batch_number TEXT,
    product_line TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


"""

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

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_TABLE_QUERY)
        connection.commit()
        cursor.close()
        print("✅ Table 'production_data' created successfully")
    except OperationalError as e:
        print(f"❌ The error '{e}' occurred")


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

