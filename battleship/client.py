#!/usr/bin/python3
'''
CSCI 466: Networks Programming Assignment 1.
Authored by Marie Morin and Hugh Jackovich.
'''
import argparse, re, requests


def main():
    parser = argparse.ArgumentParser(description='Define server IP, connection port and user\'s board.')
    parser.add_argument('server', action='store')
    parser.add_argument('port', action='store')
    parser.add_argument('x_loc', action='store')
    parser.add_argument('y_loc', action='store')
    args = parser.parse_args()

    server_ip = args.server
    port = args.port
    x_loc = args.x_loc
    y_loc = args.y_loc

    r = requests.post('http://%s:%s?x=%s&y=%s' % (server_ip, port, x_loc, y_loc))
    if r.status_code == 200:
        if "hit=1" in r.reason:
            print("Hit :)")
        elif "hit=0" in r.reason:
            print("Miss :(")
        elif "Win" in r.reason:
            print("Yay! You won the game!")
        elif "sink" in r.reason:
            print("You sank %s" % r.reason)
        update_file(int(x_loc), int(y_loc), r.reason)
    elif r.status_code == (404 or 400):
        print("Uh oh! That location doesn't exist.")
    elif r.status_code == 410:
        print("You already bombed that section.")



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
