import logging
import webbrowser
import http.server
import socketserver
import threading
import time
import os
import socket
from urllib.parse import parse_qs, urlencode, urlparse
from src.service import Service

class CodeHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        auth_code = parse_qs(urlparse(self.path).query).get('code', [None])[0]
        self.server.auth_code = auth_code
        if auth_code is not None:
            logging.info("Token received: " + auth_code)
        else:
            self.server.auth_code = False
            logging.error("Token not received")

        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<body style="background-color:black;color:white;">You can close this window now.</body>')

    def log_message(self, format, *args):
        return
    

class AAI(Service):
    def __init__(self, base_url, username=None, password=None, token=None):
        self.__client_id = 'APP-716673AA-B4AE-4E3E-83BB-D6708E810DBD'
        self.__redirect_host = 'localhost'
        self.__redirect_port = 8000
        self.__authcode = None
        self.__token = None
        super().__init__(base_url, username, password, token)

    def __get_available_port(self, start_port):
        port = start_port
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                result = sock.connect_ex((self.__redirect_host, port))
                if result != 0:
                    return port
                port += 1  

    def login(self):
        self.__redirect_port = self.__get_available_port(self.__redirect_port)

        redirect_url = 'http://{}:{}'.format(self.__redirect_host, self.__redirect_port)
        logging.info(f"Redirect URL: {redirect_url}")
        with socketserver.TCPServer((self.__redirect_host, self.__redirect_port), CodeHandler) as httpd:
            httpd.auth_code = None
            thread = threading.Thread(target=httpd.serve_forever)
            thread.daemon = True
            thread.start()

            # Wait for the server to start
            while not thread.is_alive():
                time.sleep(1)

            params = {
                'response_type': 'code',
                'scope': 'openid profile email eduperson_entitlement ga4gh_passport_v1',
                'client_id': self.__client_id,
                'state': 'StAtE',
                'redirect_uri': redirect_url
            }
            auth_url = f"https://login.elixir-czech.org/oidc/authorize?{urlencode(params)}"
            webbrowser.open(auth_url)

            # Wait for the auth code to be captured
            while httpd.auth_code is None and httpd.auth_code is not False:
                time.sleep(1)

            if httpd.auth_code is True:
                self.__authcode = httpd.auth_code

            httpd.shutdown()
            thread.join()

        if self.__authcode:
            token_url = "https://login.elixir-czech.org/oidc/token"
            token_data = {
                'grant_type': 'authorization_code',
                'code': self.__authcode,
                'redirect_uri': redirect_url,
                'client_id': self.__client_id
            }
            response = self.request('POST', token_url, data=token_data)
            response.raise_for_status() 
            self.__token = response.json()['access_token']

        token_path = os.path.expanduser('~/.ga4gh-cli.token')
        with open(token_path, 'w') as file:
            file.write(self.__token if self.__token else '')
        os.chmod(token_path, 0o600)

        return self.__token

    def logout(self):
        self.token = None
        os.remove(os.path.expanduser('~/.ga4gh-cli.token'))
        return None

    def get_userinfo(self):
        response = self.request('GET', 'userinfo') # todo: check
        return response
    
    def get_token(self):
        try:
            with open(os.path.expanduser('~/.ga4gh-cli.token'), 'r') as file:
                return file.read().strip() or None
        except FileNotFoundError:
            return None
