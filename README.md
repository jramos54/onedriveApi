# Guía de instalación y configuración

## Descomprimir onedrive_api.zip
## Dentro de la carpeta ya descomprimida:

## Creación de un entorno virtual
    python -m venv venv

## Activación del entorno virtual
    venv/Scripts/activate

## Instalación de dependencias
    pip install -r requirements.txt

## Configuración de la base de datos MySQL
    CREATE DATABASE iscam_onedrive_api;
    CREATE USER 'onedriveuser'@'localhost' IDENTIFIED BY '123456';
    GRANT ALL PRIVILEGES ON iscam_onedrive_api.* TO 'onedriveuser'@'localhost';
    FLUSH PRIVILEGES;

## Ejecución del servidor FastAPI con Uvicorn

    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
