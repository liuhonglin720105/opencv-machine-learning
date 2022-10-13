#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 17:51:11 2022

@author: zyp

"""

from dlgo import minimax
from dlgo import ttt

from six.moves import input

COL_NAMES = "ABC"

def print_board(board):
    print('   A    B   C')
    for row in (1, 2, 3):
        pieces = []
        for col in (1, 2, 3):
            piece = board.get(ttt.Point(row, col))
            if piece == ttt.Player.x:
                pieces.append('X')
            elif piece == ttt.Player.o:
                pieces.append('O')
            else:
                pieces.append(' ')
        print('%d  %s' %(row, ' | '.join(pieces)))
        
def point_from_coords(text):
    col_name = text[0]
    row = int(text[1])
    return ttt.Point(row, COL_NAMES.index(col_name) + 1)

def main():
    print('first line')
    game = ttt.GameState.new_game()
    
    human_player = ttt.Player.o
    #bot_player = ttt.Player.o
    bot = minimax.MiniMaxAgent()
    
    while not game.is_over():
        print_board(game.board)
        if game.next_player == human_player:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = ttt.Move(point)
        else:
            move = bot.select_move(game)
        game = game.apply_move(move)
    
    print_board(game.board)
    winner = game.winner()
    if winner is None:
        print("和棋")
    else:
        print('Winnder: ' + str(winner))

if __name__ == '__main__':
    main()
