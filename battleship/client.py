#!/usr/bin/python3
'''
CSCI 466: Networks Programming Assignment 1.
Authored by Marie Morin and Hughe Jackovich.
'''
import requests, argparse, socket, http.client

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Define server IP, connection port and user\'s board.')
    parser.add_argument('server', action='store')#, description='IP of the server')
    parser.add_argument('port', action='store')#, description='Port to connect to server')
    parser.add_argument('x_loc', action='store')#, description='X-axis location of fire')
    parser.add_argument('y_loc', action='store')#, description='Y-axis location of fire')
    args = parser.parse_args()                  #Had to comment these out to run

    server_ip = args.server
    port = args.port
    x_loc = args.x_loc
    y_loc = args.y_loc
    host = socket.gethostname()

    r = requests.post('http://%s:%s?x=%s&y=%s' %('localhost', port, x_loc, y_loc))
    print(r)
    conn = http.client.HTTPConnection(host, port)
    conn.request("POST", 'http://%s:%s?x=%s&y=%s' % (host, port, x_loc, y_loc))
    #response = conn.getresponse() For when we get the responses working
    #data = response.read()
    conn.close()
