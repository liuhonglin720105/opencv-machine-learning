#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 16:48:48 2022

@author: zyp
"""

import copy
from dlgo.ttt.ttttypes  import Player, Point

__all__ = [
    'Board',
    'GameState',
    'Move',
]

class IllegalMoveErrot(Exception):
    pass

BOARD_SIZE = 3
ROWS = tuple(range(1, BOARD_SIZE + 1))
COLS = tuple(range(1, BOARD_SIZE + 1))

DIAG_1 = (Point(1,1), Point(2,2), Point(3,3))
DIAG_2 = (Point(1,3), Point(2,2), Point(3,1))

class Board():
    def __init__(self):
        self._grid ={} #A dictionary you use to store strings of stones
        
    def place(self, player, point):
        assert self.is_on_grid(point) #棋子必须落在棋盘上
        assert self._grid.get(point) is None #棋子不能和已有棋子重合
        self._grid[point] = player

    
    @staticmethod    
    def is_on_grid(point):
        return 1<= point.row <= BOARD_SIZE and \
            1<= point.col <= BOARD_SIZE
    
    
    def get(self, point):
        return self._grid.get(point)


class Move(): #棋手在一轮中可以采取的行动，下棋、停一首，认输
    def __init__(self, point = None, is_pass = False, is_resign = False):
        self.point = point
        
    


                    

    
class GameState:
    def __init__(self, board, next_player, move):
        self.board = board
        self.next_player = next_player
        self.last_move = move
        
    def apply_move(self, move):
        next_board = copy.deepcopy(self.board)
        next_board.place(self.next_player, move.point)
        return GameState(next_board, self.next_player.other, move)
    
    @classmethod 
    def new_game(cls):
        board = Board()
        return GameState(board, Player.x, None)

    def is_valid_move(self, move):
        return(
            self.board.get(move.point) is None and
            not self.is_over())

    def legal_moves(self):
        moves = []
        for row in ROWS:
            for col in COLS:
                move = Move(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)
        return moves;
    
    def is_over(self):
        if self._has_3_in_a_row(Player.x):
            return True
        if self._has_3_in_a_row(Player.o):
            return True
        if all(self.board.get(Point(row, col)) is not None 
                for row in ROWS
                for col in COLS):
            return True
        return False
    
    def _has_3_in_a_row(self, player):
        # Vertical
        for col in COLS:
            if all(self.board.get(Point(row,col)) == player for row in ROWS):
                return True
        # Horizontal
        for row in ROWS:
            if all(self.board.get(Point(row,col)) == player for col in COLS):
                return True
        
        if self.board.get(Point(1,1)) == player and \
            self.board.get(Point(2,2)) == player and \
            self.board.get(Point(3,3)) == player:
            return True
        
        if self.board.get(Point(1,3)) == player and \
            self.board.get(Point(2,2)) == player and \
            self.board.get(Point(3,1)) == player:
            return True
        return False
    
    def winner(self):
        if self._has_3_in_a_row(Player.x):
            return Player.x
        if self._has_3_in_a_row(Player.o):
            return Player.o
        return None
        
                           
                    
                    
    