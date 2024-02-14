import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from services.zipfiles import ZipFiles

async def main():
    zipObject = ZipFiles('test')
    dir_resultante=await zipObject.comprimir_directorio("test_dir")
    print(dir_resultante)
    
if __name__ == "__main__":
    asyncio.run(main())