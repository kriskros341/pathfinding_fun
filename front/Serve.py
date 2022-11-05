from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

hostName = "localhost"
defaultPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        with open("result.json", "r") as f:
            self.wfile.write(bytes(f.readline(), "utf-8"))

if __name__ == "__main__":        
    arg1 = int(sys.argv[1])
    serverPort = arg1 if arg1 else defaultPort
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
