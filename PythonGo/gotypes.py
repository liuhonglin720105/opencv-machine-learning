# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 20:12:35 2022

@author: liu honglin
"""

import enum

class Player(enum.Enum):
    black = 1
    white =2
    
    @property
    def other(self):
        return Player.black if self == Player.white else Player.white
 
from collections import namedtuple 

class Point(namedtuple('Point', 'row col')):
    def neighbors(self):
        return[
                Point(self.row -1, self.col),
                Point(self.row +1, self.col),
                Point(self.row , self.col -1),
                Point(self.row , self.col +2),
                           ]
# neighbors返回上下左右四个点的坐标
# A namedtuple lets you access the coordinates as point.row and point.col 
# of point[0] and point[1]  
