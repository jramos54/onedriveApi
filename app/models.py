from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
DATABASE=os.getenv("DATABASE")
HOST_DATABASE=os.getenv("HOST_DATABASE")
DATABASE_DRIVE=os.getenv("DATABASE_DRIVE")
PORT = os.getenv("PORT_DATABASE")
DATABASE_URL = f"{DATABASE_DRIVE}://{USER}:{PASSWORD}@{HOST_DATABASE}/{DATABASE}" #{HOST_DATABASE}:{PORT}
TABLE_NAME=os.getenv("TABLE_NAME")
TABLE_USER=os.getenv("TABLE_USER")

Base = declarative_base()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class RegistroUpload(Base):
    __tablename__ = TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String(512), index=True)
    origen = Column(String(512))
    destino = Column(String(512))
    periodo = Column(String(512), index=True)
    urldestino = Column(String(512))
    fileid=Column(String(512))
    task_id=Column(String(1024))
    status=Column(String(128))
    fecha = Column(Date)    

class User(Base):
    __tablename__ = TABLE_USER

    Id = Column(Integer, primary_key=True)
    UserName = Column(String(255), unique=True, index=True)
    Password = Column(String(1024))
    
Base.metadata.create_all(bind=engine)
