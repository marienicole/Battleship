#!/usr/bin/python3
'''
CSCI 466: Networks Programming Assignment 1.
Authored by Marie Morin and Hughe Jackovich.
'''
import requests, argparse, socket, http.client

class ClientRequest:
    def __init__(self, server, port, x_addr, y_addr):
        self.server = server
        self.port = port
        self.x_addr = x_addr
        self.y_addr = y_addr
        self.send_request(self.server, self.port, self.x_addr, self.y_addr)

    def send_request(self, server, port, x_addr, y_addr):
        r = requests.post('http://%s:%s?x=%s&y=%s' %(server, port, x_addr, y_addr))
        print(r)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Define server IP, connection port and user\'s board.')
    parser.add_argument('server', action='store')
    parser.add_argument('port', action='store')
    parser.add_argument('x_addr', action='store')
    parser.add_argument('y_addr', action='store')
    args = parser.parse_args()                  #Had to comment these out to run

    server = args.server
    port = args.port
    x_addr = args.x_addr
    y_addr = args.y_addr

    c = ClientRequest(server, port, x_addr, y_addr)
