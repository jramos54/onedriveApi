from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import RegistroUpload
from app.schemas import RegistroCreate,Registro
from .zipfiles import ZipFiles
from datetime import date
from .onedrive import OneDriveApi
from .actions_one_drive import AppApiOneDrive
import os
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

async def create_onedrive(db: Session, registro_data: RegistroCreate):
    
    zipObject = ZipFiles(registro_data.file_name)
    dir_resultante = await zipObject.comprimir_directorio(registro_data.origen)
    print(dir_resultante)
    
    onedrive_api = AppApiOneDrive()
    await onedrive_api.get_token()
    await onedrive_api.get_idUser()
    await onedrive_api.get_shared_ids()
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

async def create_onedrive_lage(db: Session, registro_data: RegistroCreate, task_id: str):
    start_time = time.time()

    update_task_status(db, task_id, "Process Started")
    
    executor = ThreadPoolExecutor(max_workers=4)
    zipObject = ZipFiles(registro_data.file_name)

    try:
        dir_resultante = await asyncio.get_event_loop().run_in_executor(executor, zipObject.comprimir_directorio, registro_data.origen)
        integridad = await asyncio.get_event_loop().run_in_executor(executor, zipObject.verificar_integridad)
        
        if not integridad:
            update_task_status(db, task_id, "Failed Integrity")
            return get_task_status(db, task_id)

        update_task_status(db, task_id, "Zip Completed")
        
        print(dir_resultante)

        onedrive_api = AppApiOneDrive()
        await onedrive_api.get_token()
        await onedrive_api.get_idUser()
        await onedrive_api.get_shared_ids()

        max_retries = 5  # Número de reintentos para la carga
        for attempt in range(max_retries):
            try:
                update_task_status(db, task_id, "Uploading")
                
                path_destino = os.path.join(registro_data.destino, registro_data.file_name + '.zip')
                response_onedrive = await onedrive_api.upload_large_file(path_destino, dir_resultante)

                if response_onedrive:
                    await zipObject.eliminar_zip()
                    print(response_onedrive)

                    registro = Registro(
                        cliente=registro_data.cliente,
                        origen=registro_data.origen,
                        destino=registro_data.destino,
                        periodo=registro_data.periodo,
                        urldestino=response_onedrive.get("webUrl"),
                        fileid=response_onedrive.get("id"),
                        task_id=task_id,
                        status="Completed",
                        fecha=date.today()
                    )

                    db_registro = db.query(RegistroUpload).filter(RegistroUpload.task_id == task_id).first()
                    if db_registro:
                        # Actualizar el registro existente
                        db_registro.cliente = registro.cliente
                        db_registro.origen = registro.origen
                        db_registro.destino = registro.destino
                        db_registro.periodo = registro.periodo
                        db_registro.urldestino = registro.urldestino
                        db_registro.fileid = registro.fileid
                        db_registro.status = registro.status
                        db_registro.fecha = registro.fecha

                        db.commit()
                        db.refresh(db_registro)

                    break  # Salir del bucle si la carga es exitosa

            except Exception as e:
                print(f"Error en el intento {attempt + 1}: {e}")
                traceback.print_exc()

                if attempt < max_retries - 1:
                    print("Reintentando la carga...")
                    continue  # Intentar nuevamente
                else:
                    update_task_status(db, task_id, "Fail")
                    # Si se alcanza el máximo de reintentos, retorna el estado de la tarea
                    return get_task_status(db, task_id)

    finally:
        executor.shutdown(wait=True)
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"Tiempo de ejecución del proceso: {duration} segundos")
    return get_task_status(db, task_id)

        
    

async def create_task(db: Session, registro_data: RegistroCreate,task_id:str,status:str):
    
    registro = Registro(
        cliente=registro_data.cliente,
        origen=registro_data.origen,
        destino=registro_data.destino,
        periodo=registro_data.periodo,
        urldestino=None,
        fileid=None,
        task_id=task_id,
        status=status,
        fecha=date.today()
    )

    db_registro = RegistroUpload(
        cliente=registro.cliente,
        origen=registro.origen,
        destino=registro.destino,
        periodo=registro.periodo,
        urldestino=registro.urldestino,
        fileid=registro.fileid,
        task_id=registro.task_id,
        status=registro.status,
        fecha=registro.fecha
    )
    
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)

    return db_registro

def update_task_status(db: Session, task_id: str, status: str):
    
    db_registro = db.query(RegistroUpload).filter(RegistroUpload.task_id == task_id).first()
    if db_registro:
        db_registro.status = status
        db.commit()

def get_task_status(db: Session, task_id: str):
    registro = db.query(RegistroUpload).filter(RegistroUpload.task_id == task_id).first()
    return registro


# def delete_onedrive(db: Session, item_id: int):
#     db_registro = db.query(RegistroUpload).filter(RegistroUpload.id == item_id).first()
#     if db_registro:
#         db.delete(db_registro)
#         db.commit()
#     return db_registro
