import os
import zipfile
from pathlib import Path
import shutil  

class ZipFiles:
    def __init__(self, file_name: str):
        self.archivo_zip = f"{file_name}.zip"
        
    async def comprimir_directorio(self, directorio: str) -> str:
        with zipfile.ZipFile(self.archivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(directorio):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(directorio, '..')))
        
        ruta_final_zip = os.path.join(directorio, self.archivo_zip)
        shutil.move(self.archivo_zip, ruta_final_zip)

        return os.path.abspath(ruta_final_zip)

    async def eliminar_archivo_zip(self):
        Path(self.archivo_zip).unlink(missing_ok=True)

