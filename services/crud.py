from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import RegistroUpload
from app.schemas import RegistroCreate,Registro
from .zipfiles import ZipFiles
from datetime import date
from .onedrive import OneDriveApi
from .actions_one_drive import ApiOneDriveActions,ApiOneDriveAuthenticate,AppApiOneDrive


async def create_onedrive(db: Session, registro_data: RegistroCreate):
    onedrive_api = AppApiOneDrive()
    await onedrive_api.get_token()
    await onedrive_api.get_idUser()
    await onedrive_api.get_shared_ids()
    
    zipObject = ZipFiles(registro_data.file_name)
    dir_resultante = await zipObject.comprimir_directorio(registro_data.origen)
    print(dir_resultante)

    # onedrive_actions = ApiOneDriveActions(onedrive_api.access_token)

    # url_onedrive,fileid = await onedrive_api.upload_file(registro_data.file_name+'.zip', registro_data.destino, dir_resultante)
    url_onedrive,fileid = await onedrive_api.upload_to_shared(registro_data.file_name+'.zip', registro_data.destino, dir_resultante)

    print(url_onedrive)
    registro = Registro(
        cliente=registro_data.cliente,
        origen=registro_data.origen,
        destino=registro_data.destino,
        periodo=registro_data.periodo,
        urldestino=url_onedrive,
        fileid=fileid,
        fecha=date.today()
    )

    db_registro = RegistroUpload(
        cliente=registro.cliente,
        origen=registro.origen,
        destino=registro.destino,
        periodo=registro.periodo,
        urldestino=registro.urldestino,
        fileid=fileid,
        fecha=registro.fecha
    )
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)

    return db_registro

def get_onedrive(
    db: Session,
    item_id: Optional[int] = None,
    cliente: Optional[str] = None,
    periodo: Optional[str] = None,
    limit: int = 10,
    page: int = 1
    ):
    
    query = db.query(RegistroUpload)

    if item_id is not None:
        query = query.filter(RegistroUpload.id == item_id)

    if cliente is not None:
        query = query.filter(RegistroUpload.cliente == cliente)
        
    if cliente is not None and periodo is not None:
        query = query.filter(RegistroUpload.periodo == periodo)
        
    elif periodo is not None:
        query = query.filter(RegistroUpload.periodo == periodo)

    query = query.order_by(RegistroUpload.id)
    
    start = (page - 1) * limit
    items = query.offset(start).limit(limit).all()

    return items

# def delete_onedrive(db: Session, item_id: int):
#     db_registro = db.query(RegistroUpload).filter(RegistroUpload.id == item_id).first()
#     if db_registro:
#         db.delete(db_registro)
#         db.commit()
#     return db_registro
