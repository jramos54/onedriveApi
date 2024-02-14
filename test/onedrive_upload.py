import sys
import os,json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.onedrive import OneDriveApi
from services.actions_one_drive import ApiOneDriveAuthenticate,AppApiOneDrive
import requests
from dotenv import load_dotenv


load_dotenv()
client_id = os.getenv("CLIENT_ID")
tenant_id = os.getenv("TENANT")
client_secret = os.getenv("CLIENT_SECRET")
access_token=None
url_auth=f"https://login.microsoft.com/{tenant_id}/oauth2/token"
        
# onedrive_api = OneDriveApi()
# onedrive_api.authentication()
onedrive_api=ApiOneDriveAuthenticate()
access_token=onedrive_api.authenticate()
   
nombre_del_archivo_en_onedrive = "archivo_13-02-2024.zip"
# GAPH_URL="https://graph.microsoft.com/v1.0/me/drive/root"
# GAPH_URL="https://graph.microsoft.com/v1.0/users/3f27bfe2-2e9f-4745-a0b0-806d0a23de3a/drive/root"
GAPH_URL="https://graph.microsoft.com/v1.0/drives/b!Le2I9ta-DUqb26GNhl_PKKABivbyIeFIuu9w6jEjgmEdLpfwpRV-SqdZwuCL4kxB/items/01YFKEQH3O2VIZ4CGIMJAIS7XCRE7IRDAT"

folder_path="/Entregables ISCAM Industria/Entregables ISCAM Industria Demo 2/test_13_02_2024/"
url_de_subida = f"{GAPH_URL}:{folder_path}{nombre_del_archivo_en_onedrive}:/content"
ruta_del_archivo_local=r"C:\Users\jramos\codingFiles\dacodes\onedrive_api\test_07-02-2024.zip"



# Leer el archivo local
with open(ruta_del_archivo_local, "rb") as archivo:
    contenido_del_archivo = archivo.read()

# print(access_token)
# Configurar los headers
# headers = {
#     "Authorization": f"Bearer {onedrive_api.access_token}",
#     "Content-Type": "application/octet-stream"
# }
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/octet-stream"
}

# Realizar la petición de subida
# respuesta = requests.put(url_de_subida, headers=headers, data=contenido_del_archivo)

# print(type(respuesta.status_code))
# print(respuesta.status_code)
# # Verificar si la subida fue exitosa
# if respuesta.status_code == 200 or respuesta.status_code == 201:
#     print("\n\nArchivo subido con éxito.")
#     data=respuesta.json()
#     print(f"ubicacion del archivo:\n {data.get('webUrl')}")
#     print(f"ubicacion del archivo:\n {type(data.get('webUrl'))}")
# else:
#     print("\n\nError al subir el archivo:", respuesta.json())


url=f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

body={
    "grant_type":"client_credentials",
    "client_secret":client_secret,
    "scope":"https://graph.microsoft.com/.default",
    "client_id":client_id
}

auth=requests.post(url,data=body)
# print(auth.json()['access_token'])

access_token=auth.json()['access_token']

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# response = requests.get(f"https://graph.microsoft.com/v1.0/users/3f27bfe2-2e9f-4745-a0b0-806d0a23de3a/drive/root/children",headers=headers)
response = requests.get(f"https://graph.microsoft.com/v1.0/users/3f27bfe2-2e9f-4745-a0b0-806d0a23de3a/drive/sharedWithMe",headers=headers)
# print(json.dumps(response.json(),indent=4))

data=response.json()

drive_id=data['value'][0]['remoteItem']['parentReference']['driveId']
print(drive_id)

respuesta = requests.put(url_de_subida, headers=headers, data=contenido_del_archivo)

print(type(respuesta.status_code))
print(respuesta.status_code)
# Verificar si la subida fue exitosa
if respuesta.status_code == 200 or respuesta.status_code == 201:
    print("\n\nArchivo subido con éxito.")
    data=respuesta.json()
    print(f"ubicacion del archivo:\n {data.get('webUrl')}")
    print(f"ubicacion del archivo:\n {data.get('id')}")
else:
    print("\n\nError al subir el archivo:", respuesta.json())


############3

# async def main():
#     nombre_del_archivo_en_onedrive = "archivo_13-02-2024.zip"
#     GAPH_URL="https://graph.microsoft.com/v1.0/users/3f27bfe2-2e9f-4745-a0b0-806d0a23de3a/drive/items/01YFKEQH3O2VIZ4CGIMJAIS7XCRE7IRDAT"
#     folder_path="/Entregables ISCAM Industria/Entregables ISCAM Industria Demo 2/test_13_02_2024/"
#     url_de_subida = f"{GAPH_URL}:{folder_path}{nombre_del_archivo_en_onedrive}:/content"
#     ruta_del_archivo_local=r"C:\Users\jramos\codingFiles\dacodes\onedrive_api\test_07-02-2024.zip"

#     api=AppApiOneDrive()
#     await api.get_token()
#     await api.get_idUser()
#     # Leer el archivo local
    
#     with open(ruta_del_archivo_local, "rb") as archivo:
#         contenido_del_archivo = archivo.read()
        
        
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     response = requests.get(f"https://graph.microsoft.com/v1.0/users/3f27bfe2-2e9f-4745-a0b0-806d0a23de3a/drive/sharedWithMe",headers=headers)

#     print(json.dumps(response.json(),indent=4))


#     respuesta = requests.put(url_de_subida, headers=headers, data=contenido_del_archivo)

#     print(type(respuesta.status_code))
#     print(respuesta.status_code)
#     # Verificar si la subida fue exitosa
#     if respuesta.status_code == 200 or respuesta.status_code == 201:
#         print("\n\nArchivo subido con éxito.")
#         data=respuesta.json()
#         print(f"ubicacion del archivo:\n {data.get('webUrl')}")
#         print(f"ubicacion del archivo:\n {data.get('id')}")
#     else:
#         print("\n\nError al subir el archivo:", respuesta.json())

