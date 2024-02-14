import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import urlparse, parse_qs
import requests
from dotenv import load_dotenv

class OneDriveApi:
    def __init__(self):
        # Cargar variables de entorno
        load_dotenv()
        self.client_id = os.getenv("CLIENT_ID")
        self.tenant_id = os.getenv("TENANT")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.authority_url = "https://login.microsoftonline.com"
        self.redirect_uri = 'http://localhost:8000/callback'
        self.token_url = f"{self.authority_url}/{self.tenant_id}/oauth2/v2.0/token"
        self.access_token = None
        self.refresh_token = None

        if not self.tenant_id:
            raise ValueError("TENANT_ID no está definido. Verifica tus variables de entorno.")

    def authentication(self):
        scope = "Files.ReadWrite offline_access User.Read"
        response_type = "code"

        # Construir la URL de autenticación
        auth_url = f"{self.authority_url}/{self.tenant_id}/oauth2/v2.0/authorize?client_id={self.client_id}&response_type={response_type}&redirect_uri={self.redirect_uri}&scope={scope}&response_mode=query"
        # print("URL de autenticación:", auth_url)
        webbrowser.open_new(auth_url)

        # Crear y ejecutar un servidor HTTP para manejar el callback
        server_address = ('localhost', 8000)

        # La función lambda es utilizada para crear una instancia de CallbackHandler con la instancia de OneDriveApi como argumento
        httpd = HTTPServer(server_address, lambda *args, **kwargs: CallbackHandler(self, *args, **kwargs))
        httpd.handle_request()

    def get_token(self, code):
        data = {
            "client_id": self.client_id,
            "scope": "Files.ReadWrite offline_access User.Read",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            "client_secret": self.client_secret
        }

        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            self.access_token = response.json().get('access_token')
            self.refresh_token = response.json().get('refresh_token')
            # print("Token de acceso:", self.access_token)
            # print("Token de actualización:", self.refresh_token)
        else:
            print("Error al obtener el token de acceso:", response.text)

    def get_refresh_token(self, refresh_token):
        data = {
            "client_id": self.client_id,
            "scope": "Files.ReadWrite offline_access User.Read",
            "refresh_token": refresh_token,
            "redirect_uri": self.redirect_uri,
            "grant_type": "refresh_token",
            "client_secret": self.client_secret
        }

        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            self.access_token = response.json().get('access_token')
            self.refresh_token = response.json().get('refresh_token')
            # print("Nuevo token de acceso:", self.access_token)
            # print("Nuevo token de actualización:", self.refresh_token)
        else:
            print("Error al renovar el token de acceso:", response.text)

class CallbackHandler(BaseHTTPRequestHandler):
    def __init__(self, api_instance, *args, **kwargs):
        self.api_instance = api_instance
        super().__init__(*args, **kwargs)

    def do_GET(self):
        url_components = urlparse(self.path)
        query_components = parse_qs(url_components.query)

        code = query_components.get('code', [None])[0]
        if code:
            # print("Código de autorización obtenido:", code)
            self.api_instance.get_token(code)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Autenticacion completada. Puedes cerrar esta ventana.")

