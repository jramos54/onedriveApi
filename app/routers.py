from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from .schemas import Registro,RegistroCreate
from .models import RegistroUpload, Session
from services.crud import create_onedrive, get_onedrive


router = APIRouter()

def get_db():
    """
    Función de dependencia para obtener una instancia de la sesión de base de datos.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()

@router.post("/onedrive/", response_model=Registro)
async def create_onedrive_api(registro: RegistroCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear un registro en OneDrive.

    Args:
    
        cliente: Cliente asociado al registro.
        
        origen: Origen del registro.
        
        destino: Destino del registro.
        
        periodo: Período del registro.
        
        file_name: Nombre del archivo asociado al registro.

    Returns:
    
        cliente: Cliente asociado al registro.
        
        origen: Origen del registro.
        
        destino: Destino del registro.
        
        periodo: Período del registro.
        
        id: Identificador único del registro 
        
        urldestino: URL de destino del registro.
        
        fileid: ID del archivo asociado al registro.
        
        fecha: Fecha del registro.
    """
    return await create_onedrive(db, registro)

@router.get("/onedrive", response_model=List[Registro])
async def get_onedrive_api(
    item_id: Optional[int] = None,
    cliente: Optional[str] = None,
    periodo: Optional[str] = None,
    limit: int = 10,
    page: int = 1,
    db: Session = Depends(get_db)):
    """
    Endpoint para obtener registros de OneDrive.

    Args:
    
        item_id : ID del registro.
        
        cliente: Cliente asociado al registro.
        
        periodo : Período del registro.
        
        limit : Límite de resultados por página.
        
        page : Página solicitada.

    Returns:
        [
            {
            cliente: Cliente asociado al registro.
            
            origen: Origen del registro.
            
            destino: Destino del registro.
            
            periodo: Período del registro.
            
            id: Identificador único del registro 
            
            urldestino: URL de destino del registro.
            
            fileid: ID del archivo asociado al registro.
            
            fecha: Fecha del registro.
            }
        ]
    """
    
    return get_onedrive(db,item_id,cliente,periodo,limit,page)


# @router.delete("/onedrive/{item_id}", response_model=Registro)
# async def delete_onedrive_api(item_id: int, db: Session = Depends(get_db)):
#     return delete_onedrive(db, item_id)

