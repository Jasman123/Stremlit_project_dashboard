import psycopg2
from psycopg2 import OperationalError

# =============================
# SQL: Create Table
# =============================
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS production_data (
    id SERIAL PRIMARY KEY,
    station_name TEXT NOT NULL,
    model_type TEXT NOT NULL,
    batch_number INTEGER NOT NULL,
    tray_number INTEGER NOT NULL,
    product_line TEXT NOT NULL,
    supplier_name TEXT NOT NULL,
    ok_quantity INTEGER DEFAULT 0,
    ng_quantity INTEGER DEFAULT 0,
    operator_name TEXT NOT NULL,
    remarks TEXT,
    production_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# =============================
# Connection
# =============================
def create_connection(db_name, db_user, db_password, db_host, db_port):
    try:
        return psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
    except OperationalError as e:
        print(f"❌ Database connection error: {e}")
        return None

# =============================
# Execute Generic Query
# =============================
def execute_query(connection, query, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
    except OperationalError as e:
        print(f"❌ Query error: {e}")
        connection.rollback()

# =============================
# Table Management
# =============================
def create_production_table(connection):
    execute_query(connection, CREATE_TABLE_QUERY)

def drop_production_table(connection):
    execute_query(connection, "DROP TABLE IF EXISTS production_data;")

def clear_production_table(connection):
    execute_query(connection, "DELETE FROM production_data;")

# =============================
# CRUD OPERATIONS
# =============================
def insert_production_record(connection, data):
    insert_query = """
    INSERT INTO production_data (
        station_name,
        model_type,
        batch_number,
        tray_number,
        product_line,
        supplier_name,
        ok_quantity,
        ng_quantity,
        operator_name,
        remarks
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    values = (
        data["Station Name"],
        data["Model Type"],
        data["Batch Number"],
        data["Tray Number"],
        data["Product Line"],
        data["Supplier"],
        data["OK Quantity"],
        data["NG Quantity"],
        data["Operator Name"],
        data["Remarks"]
    )

    execute_query(connection, insert_query, values)

def update_production_record(connection, record_id, updated_fields):
    set_clause = ", ".join([f"{k} = %s" for k in updated_fields.keys()])
    values = list(updated_fields.values()) + [record_id]

    update_query = f"""
    UPDATE production_data
    SET {set_clause}
    WHERE id = %s;
    """

    execute_query(connection, update_query, values)

def delete_production_record(connection, record_id):
    delete_query = "DELETE FROM production_data WHERE id = %s;"
    execute_query(connection, delete_query, (record_id,))

from dotenv import load_dotenv  
import os
# =============================
# INITIALIZE CONNECTION

load_dotenv()

conn = create_connection(
    os.getenv("DB_NAME"),   
    os.getenv("DB_USER"),   
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_HOST"),   
    os.getenv("DB_PORT")
)
# drop_production_table(conn)
# create_production_table(conn)


# if conn:
#     print("✅ Database connection established.")
    
#     data = {
#         "Station Name": "Test Station",
#         "Model Type": "TX",
#         "Batch Number": 123,
#         "Tray Number": 1,
#         "Product Line": "Test Line",
#         "Supplier": "Test Supplier",
#         "OK Quantity": 100,
#         "NG Quantity": 5,
#         "Operator Name": "Operator A",
#         "Remarks": "Initial test record"
#     }

#     insert_production_record(conn, data)
#     print("✅ Test record inserted.")

