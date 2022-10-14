#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 13:23:55 2022

@author: zyp
"""

from __future__ import absolute_import
from collections import namedtuple

from dlgo.gotypes import Player, Point

class Territory(object):
    def __init__(self, territory_map):
        self.num_black_territory = 0
        self.num_white_territory = 0
        self.num_black_stones = 0
        self.num_white_stones = 0
        self.num_dame = 0
        self.deme_points = []
    for point, status in territory_map.items():
        if status == Player.black:
            self.num_black_stones += 1
        elif status == Player.white:
            self.num_white_stones += 1
        elif status == 'territory_b':
            self.num_black_territory +=1
        elif status == 'territory_w':
            self.num_white_territory +=1
        elif statue == 'dame':
            self.num_dame +=1
            self.dame_points.append(point)
            
class GameResult(namedtuple('GameResult', 'b w komi')):
    @property
    def winner(self):
        if self.b > self.w + self.komi:
            return Player.black
        return Player.white
    
    @property
    def winning_margin(self):
        w = self.w + self.komi
        return abs(self.b - w)
    
    def __str__(self):
        w = self.w + self.komi
        if self.b > w:
            return 'B+%.1f' %(self.b - w,)
        return ('W+%1f' %(w - self.b,)
                
def evaluate_territory(board):
    status = {}
    for r in range(1, bodar.num_rows +1):
        for c in range(1, board.num_cols +1):
            p = Point(row =r, col =c)
            if p in status:
                continue
            stone = board.get(p)
            if stone is not None:
                status[p] = board.get(p)
            else:
                group, neighbors = _collect_region(p, board)
                if len(neighbors) == 1:
                    neighbor_stones = neighbors.pop()
                    stones_str = 'b' if neighbor_stone == Player.black else 'w'
                    fill_with = 'territory_' + stone_str
                else:
                    fill_with = 'dame'
                for pos in group:
                    status[pos] = fill_with
                    
def _collect_region(start_pos, board, visited=None):
    if visited = None:
        visited = {}
    if start_pos in visited:
        return [], set()
    all _points = [start_pos]
    all_borders = set()
    visited[start_pos] = True
    here = board.get(start_pos)
    deltas = [(-1,0),(1,0), (0, -1), (0,1)]
    
                   