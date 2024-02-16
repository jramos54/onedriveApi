from typing import Optional
from datetime import date
from pydantic import BaseModel

class RegistroBase(BaseModel):
    """
    Esquema base para un registro.
    """
    cliente: str  # Cliente asociado al registro.
    origen: str   # Origen del registro.
    destino: str  # Destino del registro.
    periodo: str  # Período del registro.

class Registro(RegistroBase):
    """
    Esquema para representar un registro completo.
    """
    id: Optional[int] = None  # Identificador único del registro (opcional).
    urldestino: str  # URL de destino del registro.
    fileid: str  # ID del archivo asociado al registro.
    fecha: date  # Fecha del registro.

class RegistroCreate(RegistroBase):
    """
    Esquema para la creación de un nuevo registro.
    """
    file_name: str  # Nombre del archivo asociado al registro.
    
class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    password: str