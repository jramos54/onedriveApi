import pymssql
from dotenv import load_dotenv
import os

load_dotenv()

USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
DATABASE=os.getenv("DATABASE")
HOST_DATABASE=os.getenv("HOST_DATABASE")
DATABASE_DRIVE=os.getenv("DATABASE_DRIVE")
PORT=os.getenv("PORT_DATABASE")

try:
    conn = pymssql.connect(server=HOST_DATABASE, port=PORT, user=USER, password=PASSWORD, database=DATABASE)
    print("Conexión exitosa")
    conn.close()
except Exception as e:
    print("Error al conectar:", e)
