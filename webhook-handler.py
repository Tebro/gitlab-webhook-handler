from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import argparse
import pprint
import os
from subprocess import call
from config import config

path = ""

class GitHookHandler(BaseHTTPRequestHandler):

    def handle_payload(self, json_payload):
        #pprint.pprint(json_payload)
        if json_payload['ref'] != 'refs/heads/master':
            return False

        repo = json_payload['repository']['name']
        url = json_payload['repository']['url']

        actual_path = ""

        if repo in config:
            actual_path = config[repo]
        else:
            actual_path = "%s%s" % (path, repo)

        if os.path.isdir("%s" % actual_path):
            call("git --git-dir=%s/.git --work-tree=/%s/ pull origin master" % (actual_path, actual_path), shell=True)
        else:
            call("git clone %s %s" % (url, actual_path), shell=True)

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


path = args.path
if not path.endswith('/'):
    path += "/"

server = HTTPServer(("", args.port), GitHookHandler)
server.serve_forever()