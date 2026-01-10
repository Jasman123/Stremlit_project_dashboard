from multiprocessing.dummy import connection
import psycopg2
from psycopg2 import OperationalError

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS production_data (
    id SERIAL PRIMARY KEY,

    station_name TEXT,
    model_type INTEGER,
    batch_number INTEGER,
    tray_number INTEGER,
    product_line TEXT,
    supplier_name TEXT,
    ok_quantity INTEGER,
    ng_quantity INTEGER,
    operator_name TEXT,
    remarks TEXT,
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

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("✅ Query executed successfully")
    except OperationalError as e:
        print(f"❌ The error '{e}' occurred")

def create_production_table(connection):
    execute_query(connection, CREATE_TABLE_QUERY)

def drop_production_table(connection, table_name):
    drop_query = f"DROP TABLE IF EXISTS {table_name};"
    execute_query(connection, drop_query)

def clear_production_table(connection, table_name):
    clear_query = f"DELETE FROM {table_name};"
    execute_query(connection, clear_query)

def insert_production_record(connection, record):
    insert_query = f"""
    INSERT INTO production_data
    (station_name, model_type, batch_number, tray_number,
     product_line, supplier_name, ok_quantity, ng_quantity, operator_name, remarks)
    VALUES
    ('{record['station_name']}', {record['model_type']}, {record['batch_number']},
     {record['tray_number']}, '{record['product_line']}', '{record['supplier_name']}',
     {record['ok_quantity']}, {record['ng_quantity']}, '{record['operator_name']}' ,'{record['remarks']}')
    ;
    """
    execute_query(connection, insert_query)

def update_production_record(connection, record_id, updated_fields):
    set_clause = ", ".join(
        [f"{field} = '{value}'" for field, value in updated_fields.items()]
    )
    update_query = f"""
    UPDATE production_data
    SET {set_clause}
    WHERE id = {record_id};
    """
    execute_query(connection, update_query)

def delete_production_record(connection, record_id):
    delete_query = f"DELETE FROM production_data WHERE id = {record_id};"
    execute_query(connection, delete_query)

conn = create_connection("mydb", "postgres", "123", "localhost", "5432")
create_production_table(conn)

# reset the table
# drop_production_table(conn, "production_data")
# create_production_table(conn)
#--------------------------

#execute_query(conn, "INSERT INTO production_data (station_name, model_type, batch_number, tray_number, product_line, supplier_name, ok_quantity, ng_quantity, operator_name) VALUES ('Station A', 101, 5001, 1, 'Line 1', 'Supplier X', 480, 20, 'Operator A');")   
# clear_production_table(conn, "production_data")
# if conn:
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM production_data;")
#     rows = cur.fetchall()

#     for row in rows:
#         print(row)

#     cur.close()
#     conn.close()

