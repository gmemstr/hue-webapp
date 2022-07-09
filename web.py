#!/usr/bin/env python3
from urllib import request
import http.server
import socketserver
import os

username = os.getenv("HUE_USERNAME")
hub_ip = os.getenv("HUE_HUB_ADDRESS")
user_agent =  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
port = int(os.getenv("PORT"))

def get_lights(params):
    response = request.urlopen(hub_ip + "/api/" + username + "/lights")

    return response.read().decode('utf-8')

def post_light(params):
    response = request.urlopen(hub_ip + "/api/" + username + "/lights/")

class RootHandler(http.server.SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def _set_json_response(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self._set_response()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            api_path = f"{hub_ip}/api/{username}{self.path}"
            print(api_path)
            response = request.urlopen(api_path)
            self._set_json_response()
            self.wfile.write(response.read())

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        api_path = f"{hub_ip}/api/{username}{self.path}"
        print(api_path)
        req = request.Request(url=api_path, data=self.rfile.read(content_length),headers={ 'User-Agent': user_agent }, method='PUT')
        response = request.urlopen(req)
        result = response.read()
        self._set_json_response()
        self.wfile.write(result)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        api_path = f"{hub_ip}/api/{username}{self.path}"
        req = request.Request(url=api_path, data=self.rfile.read(content_length),headers={ 'User-Agent': user_agent }, method='POST')
        response = request.urlopen(req)
        result = response.read()
        self._set_json_response()
        self.wfile.write(result)


if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", port), RootHandler) as httpd:
        print(f"serving at port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print("server closed")
