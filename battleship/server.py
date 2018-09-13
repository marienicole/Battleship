#!/usr/bin/python3
'''
CSCI 466: Networks Programming Assignment 1.
Authored by Marie Morin and Hughe Jackovich.
'''
import requests, argparse, socket


def main():
    parser = argparse.ArgumentParser(description='Define connection port and users board.')
    parser.add_argument('port', action='store')
    parser.add_argument('board', action='store')
    args = parser.parse_args()

    port = args.port
    board_loc = args.board
    read_board(board_loc)

def read_board(board_loc):
    board = open(board_loc, "r")
    lines = board.readlines()
    for line in lines:
        print(line)

main()
