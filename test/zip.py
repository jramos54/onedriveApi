import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from services.zipfiles import ZipFiles
import time

async def main():
    directory="C:\\Users\\jramos\\codingFiles\\dacodes\\scrapping_project_iscam\\GS1\\excel_files"
    zipObject = ZipFiles('zip_comprension_5')
    dir_resultante=await zipObject.comprimir_directorio(directory)
    print(dir_resultante)
    time.sleep(60)
    await zipObject.eliminar_zip()
    
if __name__ == "__main__":
    asyncio.run(main())
    
