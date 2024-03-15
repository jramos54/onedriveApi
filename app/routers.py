from fastapi import APIRouter, Depends, HTTPException, status,BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from .schemas import Registro,RegistroCreate
from .models import RegistroUpload, Session,User
from services.crud import create_onedrive, get_onedrive, create_onedrive_lage,create_task,get_task_status
from services.authenticate_methods import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import timedelta
import uuid


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    """
    Función de dependencia para obtener una instancia de la sesión de base de datos.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)

# @router.post("/onedrive/", response_model=Registro)
# async def create_onedrive_api( registro: RegistroCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
#     """
#     Endpoint para crear un registro en OneDrive.

#     Args:
    
#         cliente: Cliente asociado al registro.
        
#         origen: Origen del registro.
        
#         destino: Destino del registro.
        
#         periodo: Período del registro.
        
#         file_name: Nombre del archivo asociado al registro.

#     Returns:
    
#         cliente: Cliente asociado al registro.
        
#         origen: Origen del registro.
        
#         destino: Destino del registro.
        
#         periodo: Período del registro.
        
#         id: Identificador único del registro 
        
#         urldestino: URL de destino del registro.
        
#         fileid: ID del archivo asociado al registro.
        
#         fecha: Fecha del registro.
#     """
#     return await create_onedrive(db, registro)

@router.get("/onedrive", response_model=List[Registro])
async def get_onedrive_api(
    item_id: Optional[int] = None,
    cliente: Optional[str] = None,
    periodo: Optional[str] = None,
    limit: int = 10,
    page: int = 1,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
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


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ Endpoint para obtener token

    Args:
        username : Usuario
        password : Contraseña

    Returns:
        access_token: Token de sesion 5 min tiempo de duracion. 
        token_type: Bearer
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.UserName}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/onedrive/large-file", response_model=Registro)
async def create_onedrive_large(
    background_tasks: BackgroundTasks, 
    registro_data: RegistroCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """ End point para subir un archivo a one drive con tamaño > 1 Gb
    
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
    
    task_id = str(uuid.uuid4())
    status_task="task created"
    response=await create_task(db,registro_data,task_id,status_task)
 
    background_tasks.add_task( create_onedrive_lage, db, registro_data, task_id)
    
    response=get_task_status(db,task_id)
    return response


@router.get("/onedrive/large-file", response_model=Registro)
async def get_upload_status(
    task_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """ Consulta del estatus de carga de un archivo mediante un task_id"""
    
    registro = get_task_status(db, task_id)
    if registro:
        return registro
    else:
        raise HTTPException(status_code=404, detail="Task not found")

