#!/usr/bin/python3
'''
CSCI 466: Networks Programming Assignment 1.
Authored by Marie Morin and Hughe Jackovich.
'''
import argparse, http.client, re


def main():
    parser = argparse.ArgumentParser(description='Define server IP, connection port and user\'s board.')
    parser.add_argument('server', action='store')  # , description='IP of the server')
    parser.add_argument('port', action='store')  # , description='Port to connect to server')
    parser.add_argument('x_loc', action='store')  # , description='X-axis location of fire')
    parser.add_argument('y_loc', action='store')  # , description='Y-axis location of fire')
    args = parser.parse_args()  # Had to comment these out to run

    server_ip = args.server
    port = args.port
    x_loc = args.x_loc
    y_loc = args.y_loc
    # host = socket.gethostname()

    conn = http.client.HTTPConnection('127.0.0.1', port)
    conn.request("POST", 'http://%s:%s?x=%s&y=%s' % (server_ip, port, x_loc, y_loc))
    response = conn.getresponse()
    print(response.status, response.reason)
    if response.status == 200:
        update_file(int(x_loc), int(y_loc), response.reason)
    conn.close()


def update_file(x, y, hit):
    opp_board = open('opponent_board.txt', 'r+')
    lines = []
    counter = 0
    for line in opp_board:
        if counter == y:
            line = list(line)
            if bool(re.search('0', hit)):
                line[x] = "O"
            else:
                line[x] = "X"
            line = ''.join(line)
        lines.append(line)
        counter += 1
    opp_board.seek(0)
    opp_board.writelines(lines)
    opp_board.close()


if __name__ == "__main__":
    main()
