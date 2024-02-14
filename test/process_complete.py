import sys
import os,json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.onedrive import OneDriveApi
from services.actions_one_drive import ApiOneDriveActions, ApiOneDriveAuthenticate
from services.zipfiles import ZipFiles
import requests
import asyncio
from msgraph import GraphServiceClient



async def main(registo_data):
    
    onedrive_api = ApiOneDriveAuthenticate()
    onedrive_api.get_token()
    
    print(onedrive_api.access_token)

    zipObject = ZipFiles(registo_data["file_name"])
    dir_resultante = await zipObject.comprimir_directorio(registo_data["origen"])
    
    
    print(f"directorio resultante:\n{dir_resultante}")
    print(type(dir_resultante))

    
    onedrive_actions = ApiOneDriveActions(onedrive_api.access_token)

    url_onedrive = await onedrive_actions.upload_file(registo_data["file_name"]+'.zip', registo_data["destino"], dir_resultante)
    print(url_onedrive)
    
if __name__=="__main__":
    registro_data={
  "cliente": "TEST",
  "origen": r"C:\Users\jramos\codingFiles\dacodes\onedrive_api\app",
  "destino": "/Entregables ISCAM Industria/Entregables ISCAM Industria Demo 1/",
  "periodo": "2024-02",
  "file_name":"test_09-02-2024"
}
    # asyncio.run(main(registro_data))
    
    auth=ApiOneDriveAuthenticate()
    token=auth.authenticate()
    
    print(token)
    
    url = "https://graph.microsoft.com/v1.0/users/rpausr_01_iscam_com"

    # Set the headers for the API call
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Send the API request and get the response
    response = requests.get(url, headers=headers)

    # Parse the response as JSON
    data = json.loads(response.text)
    print(data)