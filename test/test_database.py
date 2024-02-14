import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.models import RegistroUpload, Base  
import os

USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
DATABASE=os.getenv("DATABASE")
TEST_DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@localhost:3306/{DATABASE}"

@pytest.fixture(scope="module")
def engine():
    return create_engine(TEST_DATABASE_URL)

@pytest.fixture(scope="module")
def session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_connection(engine):
    # Intenta conectar a la base de datos
    try:
        conn = engine.connect()
        conn.close()
        assert True
    except SQLAlchemyError:
        assert False

def test_insert_registro(session):
    # Intenta insertar un registro
    new_registro = RegistroUpload(cliente="Cliente Prueba", origen="Origen Prueba", destino="Destino Prueba", periodo="2024-01", urldestino="http://example.com", fecha="2024-01-01")
    session.add(new_registro)
    session.commit()

    inserted_registro = session.query(RegistroUpload).filter_by(cliente="Cliente Prueba").first()
    assert inserted_registro is not None
    assert inserted_registro.origen == "Origen Prueba"
