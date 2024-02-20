import sys
import os,json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.onedrive import OneDriveApi
from services.actions_one_drive import AppApiOneDrive
import requests
from dotenv import load_dotenv
import asyncio

async def main():
    onedrive_api = AppApiOneDrive()

    await onedrive_api.get_token()
    await onedrive_api.get_idUser()
    await onedrive_api.get_shared_ids()
    # await onedrive_api.upload_large_file('large_files/hexArq.mp4', r'C:\Users\jramos\Downloads\HexArq.mp4')
    # C:\\Users\\jramos\\codingFiles\\dacodes\\scrapping_project_iscam\\GS1\\excel_files
    response=await onedrive_api.upload_large_file('large_files/zipfile_2.zip', r'C:\Users\jramos\codingFiles\dacodes\scrapping_project_iscam\GS1\excel_files\zipfile.zip')
    print()
    print(response.get("webUrl"))
    print(response.get("id"))
if __name__=="__main__":
    
    asyncio.run(main())