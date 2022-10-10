import copy
from dlgo.gotypes import Player
from dlgo import zobrist

class Move(): #棋手在一轮中可以采取的行动，下棋、停一首，认输
    def __init__(self, point = None, is_pass = False, is_resign = False):
        assert(point is not None) ^ is_pass ^ is_resign 
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point): #在棋盘上落下一子
        return Move(point=point)
    
    @classmethod 
    def pass_turn(cls): #停一手
        return Move (is_pass = True) 
    
    @classmethod 
    def resign(cls):
        return Move(is_resign = True) #认输
    
    #程序一般不直接调用Move的构造函数，而是调用Move.play, Move.pass_turn或者
    #Move.resign来创建move的实例


class GoString(): #一块棋
    def __init__(self, color, stones, liberties): # Go strings are a chain of connected stones of the same color
        self.color = color
        self.stones = frozenset(stones)
        self.liberties = frozenset(liberties)
        
#    def remove_liberty(self,point):
#        self.liberties.remove(point) 

    def without_liberty(self, point):
        new_liberties = self.liberties - set([point])
        return GoString(self.color, self.stones, new_liberties)

        
    def with_liberty(self,point):
        new_liberties = self.liberties | set([point])
        return GoString(self.color, self.stones, new_liberties)
        
    def merge_with(self, go_string):
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones)
    
    @property
    def num_liberties(self):
        return len(self.liberties)
    
    def __eq__(self, other):
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.iberties
            

                    
class Board():
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid ={} #A dictionary you use to store strings of stones
        self._hash = zobrist.EMPTY_BOARD
        
    def place_stone(self, player, point):
        assert self.is_on_grid(point) #棋子必须落在棋盘上
        assert self._grid.get(point) is None #棋子不能和已有棋子重合
        adjacent_same_color = [] #相邻同色的棋块
        adjacent_opposite_color = [] #相邻异色棋块
        liberties = [] # 气
        for neighbor in point.neighbors():
            if not self.is_on_grid(neighbor): #相邻棋子不在棋盘上，跳过
                continue
            neighbor_string = self._grid.get(neighbor) #寻找相邻棋块
            if neighbor_string is None:
                liberties.append(neighbor) #如果相邻位置没有其他棋块，添加一气
            elif neighbor_string.color == player:   #如果相邻的棋块颜色一致，添加到相邻同色棋块中           
                if neighbor_string not in adjacent_same_color:
                    adjacent_same_color.append(neighbor_string)
            else:
                if neighbor_string not in adjacent_opposite_color: #否则添加到异色棋块集合中
                    adjacent_opposite_color.append(neighbor_string)
        new_string = GoString(player,[point],liberties)
        
        for same_color_string in adjacent_same_color:
            new_string = new_string.merge_with(same_color_string) #合并同色棋块
        for new_string_point in new_string.stones: #在字典里添加new_string_point: new_string
            self._grid[new_string_point] = new_string
        for other_color_string in adjacent_opposite_color: #相邻异色棋块去掉一气
            other_color_string.remove_liberty(point)
        for other_color_string in adjacent_opposite_color: #如果气等于零，提子
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)
                
    def _remove_string(self, string):
        for point in string.stones:
            for neighbor in point.neighbors():
                neighbor_string = self._grid.get(neighbor)
                if neighbor_string is None:
                    continue
                if neighbor_string is not string:#如果相邻棋块不是当前棋块，增加一气
                    neighbor_string.add_liberty(point)
            self._grid[point] = None
        
    def is_on_grid(self,point):
        return 1<= point.row <= self.num_rows and \
            1<= point.col <= self.num_cols
        
    def get(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color
    
    def get_go_string(self, point):
        string = self._grid.get(point)
        if string is None:
            return None
        return string
    
class GameState():
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move
        
    def apply_move(self, move):
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)
    
    @classmethod 
    def new_game(cls, board_size):
        if isinstance(board_size, int):
            board_size = (board_size, board_size)
        board = Board(*board_size)
        return GameState(board, Player.black, None, None)
    
    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move 
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass
  
    def is_move_self_capture(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0
    
    @property 
    def situation(self):
        return (self.next_player, self.board)
    
    def does_move_violate_ko(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)
        past_state = self.previous_state 
        while past_state is not None:
            if past_state.situation == next_situation:
                return True
            past_state = past_state.previous_state 
        return  False

    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return(
            self.board.get(move.point) is None and
            not self.is_move_self_capture(self.next_player, move) and
            not self.does_move_violate_ko(self.next_player, move))
            

                
                    
    