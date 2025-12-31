from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

load_dotenv()

USER = os.getenv("user")
PASSWORD = quote_plus(os.getenv("password"))  # ⬅️ penting
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
)

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("✅ Connection successful!")
except Exception as e:
    print("❌ Failed to connect:", e)
