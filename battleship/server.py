#!/usr/bin/python3
'''
CSCI 466: Networks Programming Assignment 1.
Authored by Marie Morin and Hughe Jackovich.
'''
import requests, argparse, socket
from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    #may need a set_header function?
    #Also default here to return HTTP OK?
    def do_POST(self):
        print("Handles POST requests")
        #this works from server -> client
    def do_GET(self):
        print("Handles GET requests")
        #probably return the board.txt?
    #This'll handle HTTP requests/responses by invoking BaseHTTPRequestHandler


def main():
    parser = argparse.ArgumentParser(description='Define connection port and users board.')
    parser.add_argument('port', action='store')
    parser.add_argument('board', action='store')
    args = parser.parse_args()

    port = int(args.port) #may wanna put try on this later
    board_loc = args.board
    host = socket.gethostname() #Don't think this means we have to close the socket
    read_board(board_loc)

    initServer(host, port)


def read_board(board_loc):
    board = open(board_loc, "r")
    lines = board.readlines()
    for line in lines:
        print(line)

def initServer(host, port):
    address = (host, port) #tuple forms address of the server
    handler = RequestHandler
    http_client = HTTPServer(address, handler)
    http_client.serve_forever()

main()
