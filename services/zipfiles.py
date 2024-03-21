import os
import zipfile
from pathlib import Path
import shutil , logging, time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ZipFiles:
    def __init__(self, file_name: str):
        self.archivo_zip = f"{file_name}.zip"
        
    def comprimir_directorio(self, directorio: str) -> str:
        carpeta_temporal = "temporales"
        if not os.path.exists(carpeta_temporal):
            os.makedirs(carpeta_temporal)
            logging.info(f"Carpeta temporal '{carpeta_temporal}' creada")
        
        inicio = time.time() 
        logging.info(f"Iniciando la compresión del directorio {directorio}")
        
        with zipfile.ZipFile(os.path.join(carpeta_temporal, self.archivo_zip), 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directorio):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(directorio, '..')))
                    logging.info(f"Archivo {file} agregado al zip")
        
        duracion = time.time() - inicio 
        logging.info(f"Directorio {directorio} comprimido en {duracion:.2f} segundos")
                   
        return os.path.abspath(os.path.join(carpeta_temporal, self.archivo_zip))

    
    def verificar_integridad(self) -> bool:
        with zipfile.ZipFile(os.path.join("temporales", self.archivo_zip), 'r') as zipf:
            try:
                zipf.extractall("temporales/extracted")
                return True
            except Exception as e:
                print(f"Error al extraer el archivo ZIP: {e}")
                return False
            finally:
                shutil.rmtree("temporales/extracted", ignore_errors=True)
            
    async def eliminar_zip(self):
        Path(os.path.join("temporales", self.archivo_zip)).unlink(missing_ok=True)


