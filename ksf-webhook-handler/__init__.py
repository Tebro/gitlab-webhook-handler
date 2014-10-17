from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import argparse
import pprint
import os


class GitHookHandler(BaseHTTPRequestHandler):

    def set_path(self, path):
        self.project_path = path

    def handle_payload(self, json_payload):
        pprint.pprint(json_payload)


    def do_POST(self):
        data_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(data_length)

        payload = json.loads(post_data.decode('utf-8'))
        self.handle_payload(payload)
        self.send_response(200)


argparser = argparse.ArgumentParser(description="Git hook handler.")
argparser.add_argument('port', type=int, help="TCP port to listen on.")
argparser.add_argument('path', type=str, help="Path to projects root.")
args = argparser.parse_args()

handler = GitHookHandler()
handler.set_path(args.path)

server = HTTPServer(("", args.port), handler)
server.serve_forever()