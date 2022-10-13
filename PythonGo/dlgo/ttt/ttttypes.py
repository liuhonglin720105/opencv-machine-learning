#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 16:45:13 2022

@author: zyp
"""

import enum
from collections import namedtuple

class Player(enum.Enum):
    x = 1
    o =2
    
    @property
    def other(self):
        return Player.x if self == Player.o else Player.o
    
class Point(namedtuple('Point', 'row col')):
    def __deepcopy__(self, memodict ={}):
        return self