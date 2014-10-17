gitlab-webhook-handler
======================

A small python script that parses gitlab POST requests and deploys projects into a predefined directory.

Usage: python webhook-handler.py port pathToParent

port: the port that the HTTP handler will listen on.
pathToParent: the directory where the projects will be deployed.
