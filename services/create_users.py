import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User
from authenticate_methods import get_password_hash
import argparse


USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
DATABASE=os.getenv("DATABASE")
HOST_DATABASE=os.getenv("HOST_DATABASE")
DATABASE_DRIVE=os.getenv("DATABASE_DRIVE")
PORT = os.getenv("PORT_DATABASE")
DATABASE_URL = f"{DATABASE_DRIVE}://{USER}:{PASSWORD}@{HOST_DATABASE}/{DATABASE}" #{HOST_DATABASE}:{PORT}

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_user(username: str, password: str):
    db = SessionLocal()
    hashed_password = get_password_hash(password)
    db_user = User(UserName=username, Password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Crear un nuevo usuario en la base de datos.")
    parser.add_argument("username", type=str, help="Nombre de usuario")
    parser.add_argument("password", type=str, help="Contraseña")

    args = parser.parse_args()

    create_user(args.username, args.password)