# Guía de instalación y configuración

## Descomprimir onedrive_api.zip
## Dentro de la carpeta ya descomprimida:

## eliminar el entorno virtual anterior (Solo para cuando se cambia de MySQL a SQL server)
    rm -r venv
## Creación de un entorno virtual
    python -m venv venv
## Actualizar pip
    python -m pip install --upgrade pip
## Activación del entorno virtual
    venv/Scripts/activate

## Instalación de dependencias
    pip install -r requirements.txt

## Configuración de la base de datos MySQL <- SOLO MYSQL
    CREATE DATABASE iscam_onedrive_api;
    CREATE USER 'onedriveuser'@'localhost' IDENTIFIED BY '123456';
    GRANT ALL PRIVILEGES ON iscam_onedrive_api.* TO 'onedriveuser'@'localhost';
    FLUSH PRIVILEGES;

## Actualizar los valores del archivo .env

## Ejecución del servidor FastAPI con Uvicorn

    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
