import aiohttp,json, os
from dotenv import load_dotenv
import requests
import msal



class ApiOneDriveActions:
    def __init__(self, access_token) -> None:
        self.access_token = access_token
        self.GRAPH_URL = "https://graph.microsoft.com/v1.0/me/drive/root"

    async def upload_file(self, onedrivefile, onedrivepath, localpath):
        url_onedrive = f"{self.GRAPH_URL}:{onedrivepath}{onedrivefile}:/content"
        
        raw_dir=r"{}".format(localpath)

        try:
            with open(localpath, "rb") as archivo:
                file = archivo.read()
        except IOError as e:
            return {"detail": "Error al leer el archivo local", "error": str(e)}

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/octet-stream"
        }

        async with aiohttp.ClientSession() as session:
            async with session.put(url_onedrive, headers=headers, data=file) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    print(json.dumps(data))
                    return  data.get('webUrl'), data.get('id')
                    
                else:
                    return {
                        "detail": "Error al subir el archivo",
                        "data": await response.json()
                    }
                    
class ApiOneDriveAuthenticate:
    def __init__(self) -> None:
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.tenant_id = os.getenv("TENANT")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.access_token=None
        self.url_auth=f"https://login.microsoft.com/{self.tenant_id}/oauth2/token"
        self.redirect_uri = 'http://localhost:8000/callback'
    
    # def get_token(self):
    #     data={
    #         "grant_type":"client_credentials",
    #         "client_id":self.client_id,
    #         "client_secret":self.client_secret,
    #         "resource":"https://graph.microsoft.com"
    #     }
        
    #     response = requests.post(self.url_auth, data=data)
        
    #     if response.status_code == 200:
    #         response_data=response.json()
    #         self.access_token=response_data.get("access_token",None)
    #     else:
    #         print(response.json())
    
    def authenticate(self):
        tenantID = self.tenant_id
        authority = 'https://login.microsoftonline.com/' + tenantID
        clientID = self.client_id
        clientSecret = self.client_secret
        scope = ['https://graph.microsoft.com/.default']
        app = msal.ConfidentialClientApplication(clientID, authority=authority, client_credential = clientSecret)
        response = app.acquire_token_for_client(scopes=scope)
        return response.get('access_token')


class AppApiOneDrive:
    def __init__(self) -> None:
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.tenant_id = os.getenv("TENANT")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.iscam_user = os.getenv("USER_ISCAM")
        self.access_token = None
        self.id_user = None
        self.drive_shared_id=None
        self.shared_id=None
        

    async def get_token(self):
        TOKEN_URL = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        body = {
            "grant_type": "client_credentials",
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "client_id": self.client_id
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(TOKEN_URL, data=body) as response:
                resp = await response.json()
                self.access_token = resp['access_token']

    async def get_idUser(self):
        ID_USER_URL = f"https://graph.microsoft.com/v1.0/users/{self.iscam_user}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(ID_USER_URL, headers=headers) as response:
                resp = await response.json()
                print(resp)
                self.id_user = resp['id']

    async def upload_file(self, onedrivefile, onedrivepath, localpath):
        GAPH_URL = f"https://graph.microsoft.com/v1.0/users/{self.id_user}/drive/root"
        url_de_subida = f"{GAPH_URL}:{onedrivepath}{onedrivefile}:/content"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        try:
            with open(localpath, "rb") as archivo:
                file = archivo.read()
        except IOError as e:
            return {"detail": "Error al leer el archivo local", "error": str(e)}

        async with aiohttp.ClientSession() as session:
            async with session.put(url_de_subida, headers=headers, data=file) as response:
                if response.status in [200, 201]:
                    print("\n\nArchivo subido con éxito.")
                    data = await response.json()
                    print(f"ubicacion del archivo:\n {data.get('webUrl')}")
                    print(f"ubicacion del archivo:\n {data.get('id')}")
                    return data.get('webUrl'), data.get('id')
                else:
                    resp = await response.json()
                    print("\n\nError al subir el archivo:", resp)
    
    async def upload_to_shared(self, onedrivefile, onedrivepath, localpath):
        GAPH_URL = f"https://graph.microsoft.com/v1.0/drives/{self.drive_shared_id}/items/{self.shared_id}"
        url_de_subida = f"{GAPH_URL}:{onedrivepath}{onedrivefile}:/content"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        try:
            with open(localpath, "rb") as archivo:
                file = archivo.read()
        except IOError as e:
            return {"detail": "Error al leer el archivo local", "error": str(e)}

        async with aiohttp.ClientSession() as session:
            async with session.put(url_de_subida, headers=headers, data=file) as response:
                if response.status in [200, 201]:
                    print("\n\nArchivo subido con éxito.")
                    data = await response.json()
                    print(f"ubicacion del archivo:\n {data.get('webUrl')}")
                    print(f"ubicacion del archivo:\n {data.get('id')}")
                    return data.get('webUrl'), data.get('id')
                else:
                    resp = await response.json()
                    print("\n\nError al subir el archivo:", resp)
    
    async def get_shared_ids(self):
        ID_SHARED_URL = f"https://graph.microsoft.com/v1.0/users/{self.id_user}/drive/sharedWithMe"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(ID_SHARED_URL, headers=headers) as response:
                resp = await response.json()
                self.drive_shared_id = resp['value'][0]['remoteItem']['parentReference']['driveId']
                self.shared_id= resp['value'][0]['id']
                print(self.drive_shared_id)
                print(self.shared_id)
    
