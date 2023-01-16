from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time
import json
import sys
import glob


hostName = "localhost"
defaultServerPort = 8080
bups_dir_name = "bups"
prefix_length = 2
bups_prefix_length = len(bups_dir_name) + prefix_length
data_suffix = ".detailed.json"
new_paths = {}
current_file_path = "./result.detailed.json"

class MyServer(BaseHTTPRequestHandler):
    def universal_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.send_header("Access-Control-Allow-Origin", "*")
    def do_GET(self):
        if self.path.startswith("/api"):
            if self.path.endswith("/api"):
                self.universal_headers()
                self.end_headers()
                content = json.dumps(list(new_paths.keys()))
                self.wfile.write(bytes(content, "UTF-8"))
            elif self.path.endswith("/result"):
                self.universal_headers()
                self.end_headers()
                with open(f"result{data_suffix}", "r") as f:
                    print(self.path)
                    content = f.read()
                    self.wfile.write(bytes(content, "UTF-8"))
            else:
                filename=self.path[4:]
                file = new_paths.get(filename)
                if file:
                    with open(file, "r") as f:
                        self.universal_headers()
                        self.end_headers()
                        content = f.read()
                        self.wfile.write(bytes(content, "UTF-8"))

if __name__ == "__main__":
    serverPort = sys.argv[1]
    serverPort = int(serverPort) if int(serverPort) else defaultServerPort
    additional_paths = glob.glob(f"./{bups_dir_name}/*")

    for file in additional_paths:
        if file.endswith(data_suffix):
            filename_ext = file[bups_prefix_length:]
            filename = filename_ext.removesuffix(data_suffix)
            new_paths[filename] = file
    
    current_file_path = glob.glob(f"./result{data_suffix}")

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
