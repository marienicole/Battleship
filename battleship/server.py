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
        self.board = ""

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
        # use socket/threading instead? We are always going to be on localhost
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))


    def handle_client(self, client):
        request = client.recv(1024)
        resp = self.verify(request, client)
        # this response needs to be edited so it sends whatever verify hands us
        # if it's OK, we also need to add another line to the response.
        # Maybe a separate function to handle writing the response?
        client.send(resp)


    def verify(self, request, client):
        # this function needs to validate the input and send the appropriate
        # response to the client:
        # 1. HTTP Ok --> Hit/sunk
        # 2. HTTP Not Found --> out of bounds
        # 3. HTTP Gone --> already fired upon
        # 4. HTTP Bad Request --> improper format
        return "that looks great, wow"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Define connection port and users board.')
    parser.add_argument('port', action='store')
    parser.add_argument('board', action='store')
    args = parser.parse_args()
    port = int(args.port)
    board_loc = args.board

    s = Server(port, board_loc)
