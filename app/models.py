from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
DATABASE=os.getenv("DATABASE")
DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@localhost:3306/{DATABASE}"

Base = declarative_base()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class RegistroUpload(Base):
    __tablename__ = "upload_table"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String(512), index=True)
    origen = Column(String(512))
    destino = Column(String(512))
    periodo = Column(String(512), index=True)
    urldestino = Column(String(512))
    fileid=Column(String(512))
    fecha = Column(Date)    

Base.metadata.create_all(bind=engine)
