#!/usr/bin/python3
'''
CSCI 466: Networks Programming Assignment 1.
Authored by Marie Morin and Hugh Jackovich.
'''
import re, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from time import sleep


class BattleshipServer(BaseHTTPRequestHandler):

    def do_POST(self):
        hit = self.parse_url(self.path)
        if hit == "Gone":
            self.gone_response(hit)
        else:
            self.response(hit)

    def do_GET(self):
        self.response("OK")
        if bool(re.search('own', self.path)):
            file = open('own_board.txt', 'rb')
        else:
            file = open('opponent_board.txt', 'rb')

        data = file.read()
        utf_data= data.decode('utf8').replace('\n', '<br>')
        binary_data = utf_data.encode('utf-8')

        self.send_response(200)
        self.wfile.write(binary_data)

        file.close()
        return

    def response(self, msg=None):
        self.send_response(200, msg)
        self.end_headers()

    def bad_request(self, msg=None):
        self.send_response(400, msg)
        self.end_headers()

    def not_found(self):
        self.send_response(404)
        self.end_headers()

    def gone_response(self, msg=None):
        self.send_response(410, msg)
        self.end_headers()

    def parse_url(self, url):
        if len(url) > 9:
            self.not_found()
        else:
            coords = []
            for count in range(len(url)):
                if url[count] == '=':
                    coords.append(url[count+1])

            coords = [int(i) for i in coords] # list comprehension to change to int list

            if all((i < 10) and (i > -1) for i in coords):  # makeshifty, we'll want to protect the type casting
                return board.calibrate_shot(coords[0], coords[1])  # or return value & move on from there if option route
            else:
                self.not_found()


class Board:

    def __init__(self):
        self.ship_health = {'C': 5, 'B': 4, 'R': 3, 'S': 3, 'D': 2}
        self.player_board = None
        self.opp_board = []

        for y_count in range(10):
            line = []
            for x_count in range(10):
                line.append('_')
            self.opp_board.append(line)

    def get_hits(self, ship):
        return self.ship_health[ship]

    def reduce_health(self, ship):
        self.ship_health[ship] -= 1
        if self.ship_health[ship] == 0:
            return True
        return False

    def calibrate_shot(self, x, y):
        # Duplicate hit check
        if self.opp_board[y][x] != '_':
            return "Gone"

        # handles detecting hit
        player_board = open(self.player_board, 'r')
        player_board.seek(0)
        lines = player_board.readlines()
        row = list(lines[y])
        hit = row[x]
        player_board.close()
        if hit == '_':
            self.update_opp_board(False, x, y)
            return "hit=0"
        else:
            self.update_opp_board(True, x, y)
            if self.reduce_health(hit):
                if self.check_winner():
                    return "hit=1&\sink=%s&\Win\n" % hit
                else:
                    return "hit=1&\sink=%s" % hit
            return "hit=1"

    def check_winner(self):
        for value in self.ship_health:
            if self.ship_health[value] != 0:
                return False
        return True

    def update_opp_board(self, switch, x, y):
        if switch:
            self.opp_board[y][x] = "O"
        else:
            self.opp_board[y][x] = "X"

    def setfile(self, filename):
        self.player_board = filename

    def getfile(self, filename):
        if self.player_board == filename:
            return self.player_board
        elif self.opp_board:
            return self.opp_board
        else:
            return "File Not Found"


def main():
    parser = argparse.ArgumentParser(description='Define connection port and users board.')
    parser.add_argument('port', action='store')
    parser.add_argument('board', action='store')
    args = parser.parse_args()

    port = int(args.port)  # may wanna put try on this later
    host = 'localhost'  # Don't think this means we have to close the socket
    print("serving at: %s:%s" % (host, port))
    board_loc = args.board

    board.setfile(board_loc)

    init_server(host, port)


def init_server(host, port):
    address = (host, port)  # tuple forms address of the server
    handler = BattleshipServer

    http_server = HTTPServer(address, handler)

    http_server.serve_forever()


if __name__ == '__main__':
    global http_server
    board = Board()
    main()
