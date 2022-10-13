#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 14:16:06 2022

@author: zyp
"""

#from dlgo import agent
from dlgo import goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import time
from dlgo.agent.naive import RandomBot

def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bots = {
        gotypes.Player.black: RandomBot(),
        gotypes.Player.white: RandomBot(),}
    while not game.is_over():
        time.sleep(0.1)
        
        print(chr(27) + "[2J")
        
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)
        
        
if __name__ == '__main__':
    main()
        
        
