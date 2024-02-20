import os
import zipfile
from pathlib import Path
import shutil 

class ZipFiles:
    def __init__(self, file_name: str):
        self.archivo_zip = f"{file_name}.zip"
        
    async def comprimir_directorio(self, directorio: str) -> str:
        carpeta_temporal = "temporales"
        if not os.path.exists(carpeta_temporal):
            os.makedirs(carpeta_temporal)
        
        with zipfile.ZipFile(os.path.join(carpeta_temporal, self.archivo_zip), 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directorio):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(directorio, '..')))
        
        return os.path.abspath(os.path.join(carpeta_temporal, self.archivo_zip))

    async def eliminar_zip(self):
        Path(os.path.join("temporales", self.archivo_zip)).unlink(missing_ok=True)


