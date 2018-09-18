#!/usr/bin/python3
'''
CSCI 466: Networks Programming Assignment 1.
Authored by Marie Morin and Hughe Jackovich.
'''
import requests, argparse, socket
from http.server import HTTPServer, BaseHTTPRequestHandler


class BattleshipServer(BaseHTTPRequestHandler):

    def do_POST(self):
        hit = self.parse_url(self.path)
        if hit == 1:
            self.response("hit=1")
        else:
            self.response("hit=0")



    def do_GET(self):
        print("Handles GET requests")

    def response(self, msg=None):
        self.send_response(200, msg)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def bad_request(self):
        self.send_response(400)
        self.end_headers()

    def not_found(self):
        self.send_response(404)
        self.end_headers()

    def parse_url(self, url):

        coords = []
        for count in range(len(url)):
            if url[count] == '=':
                coords.append(url[count+1])

        coords = [int(i) for i in coords] # list comprehension to change to int list

        if all((i < 11) and (i > -1) for i in coords): # makeshifty, we'll want to protect the type casting
            return self.fire_shot(coords[0], coords[1]) # or return value & move on from there if option route
        else:
            self.bad_request()

    def fire_shot(self, x, y):
        # check opp_board for it maybe? to not allow duplicate spots hit?

        # handles updating opponent_board.txt for hits
        opp_board = open('opponent_board.txt', 'r+')
        lines = []
        counter = 0
        for line in opp_board:
            if counter == y:
                line = list(line)
                line[x] = "X"
                line = ''.join(line)
            lines.append(line)
            counter += 1
        opp_board.seek(0)
        opp_board.writelines(lines)
        opp_board.close()

        # handles detecting hit
        player_board = open('own_board.txt', 'r')
        player_board.seek(0)
        lines = player_board.readlines()
        row = list(lines[y])
        hit = row[x]
        player_board.close()
        if hit == '_':
            return 0
        else:
            return 1


def main():
    parser = argparse.ArgumentParser(description='Define connection port and users board.')
    parser.add_argument('port', action='store')
    parser.add_argument('board', action='store')
    args = parser.parse_args()

    port = int(args.port) # may wanna put try on this later
    print("serving at port: ", port)
    board_loc = args.board
    host = socket.gethostname() # Don't think this means we have to close the socket
    read_board(board_loc)

    initServer(host, port)


def read_board(board_loc):
    # may be best to init opponent_board.txt here too?
    board = open(board_loc, "r")
    lines = board.readlines()
    for line in lines:
        print(line)


def initServer(host, port):
    address = (host, port) # tuple forms address of the server
    handler = BattleshipServer
    http_client = HTTPServer(address, handler)
    http_client.serve_forever()


if __name__ == '__main__':
    main()