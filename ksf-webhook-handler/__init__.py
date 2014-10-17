from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import argparse
import pprint
import os
from subprocess import call


class GitHookHandler(BaseHTTPRequestHandler):

    def set_path(self, path):
        self.projects_path = path

    def handle_payload(self, json_payload):
        #pprint.pprint(json_payload)
        if json_payload['ref'] != 'refs/heads/master':
            return False

        repo = json_payload['repository']['name']
        url = json_payload['repository']['url']

        if os.path.isdir("%s%s" % (self.projects_path, repo)):
            call("git --git-dir=%s%s/.git pull origin master" % (self.projects_path, repo), shell=True)
        else:
            call("git clone %s %s%s" % (url, self.projects_path, repo), shell=True)



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

path = args.path
if not path.endswith('/'):
    path += "/"

handler.set_path(path)

server = HTTPServer(("", args.port), handler)
server.serve_forever()