from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import argparse
import pprint

class GitHookHandler(BaseHTTPRequestHandler):

    def handle_payload(self, json_payload):
        print("JSON payload")
        pprint.pprint(json_payload)

    def do_POST(self):
        data_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(data_length)

        payload = json.loads(post_data.decode('utf-8'))
        self.handle_payload(payload)
        self.send_response(200)


argparser = argparse.ArgumentParser(description="Git hook handler")
argparser.add_argument('port', type=int, help="TCP port to listen on", default=8000)
args = argparser.parse_args()

server = HTTPServer(("", args.port), GitHookHandler)
server.serve_forever()