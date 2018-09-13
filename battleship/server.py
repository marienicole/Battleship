#!/usr/bin/python3
'''
CSCI 466: Networks Programming Assignment 1.
Authored by Marie Morin and Hughe Jackovich.
'''
import requests, argparse, socket, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class Server:
    def __init__(self, port, board_loc):
        self.port = port
        self.board_loc = board_loc

        self.read_board(board_loc)
        self.initServer('localhost', port)
        self.server.listen(port)

        while True:
            client, addr = self.server.accept()
            ''' this creates a client thread, to handle/listen on whataever port we specify '''
            client_handler = threading.Thread(target = self.handle_client, args = (client,))
            client_handler.start()


    def read_board(self, board_loc):
        board = open(board_loc, "r")
        lines = board.readlines()
        for line in lines:
            line = list(line)
        self.board = lines


    def initServer(self, host, port):
        # address = (host, port) #tuple forms address of the server
        # handler = RequestHandler
        # http_client = HTTPServer(address, handler)
        # http_client.serve_forever()

        # use socket/threading instead? We are always going to be on localhost
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))


    def handle_client(self, client):
        request = client.recv(1024)
        print(request)
        # we will want to see what the client is sending here





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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Define connection port and users board.')
    parser.add_argument('port', action='store')
    parser.add_argument('board', action='store')
    args = parser.parse_args()
    port = int(args.port)
    board_loc = args.board

    s = Server(port, board_loc)
