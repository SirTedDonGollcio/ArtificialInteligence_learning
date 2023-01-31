from dataclasses import fields
from two_player_games.move import Move
from typing import Iterable, List, Optional, Tuple
from two_player_games.game import Game
from two_player_games.player import Player
from two_player_games.state import State
import math

class ConnectFour(Game):
    """Class that represents the hex game"""
    FIRST_PLAYER_DEFAULT_CHAR = '1'
    SECOND_PLAYER_DEFAULT_CHAR = '2'

    def __init__(self, size: Tuple[int, int] = (7, 6), first_player: Player = None, second_player: Player = None):
        """
        Initializes game.

        Parameters:
            size: the size of the game as number of columns and rows
            first_player: the player that will go first (if None is passed, a player will be created)
            second_player: the player that will go second (if None is passed, a player will be created)
        """
        self.first_player = first_player or Player(self.FIRST_PLAYER_DEFAULT_CHAR)
        self.second_player = second_player or Player(self.SECOND_PLAYER_DEFAULT_CHAR)

        state = ConnectFourState(size, self.first_player, self.second_player)
        super().__init__(state)


class ConnectFourMove(Move):
    """
    Class that represents a move in the dots and boxes game

    Variables:
        column: index of the column to put the token to
    """
    def __init__(self, column) -> None:
        self.column = column
        super().__init__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConnectFourMove):
            return False
        return self.column == other.column


class ConnectFourState(State):
    """Class that represents the state of the hex game"""

    def __init__(
        self, size: Tuple[int, int] = None, current_player: Player = None, other_player: Player = None,
        fields: List[List[Player]] = None
    ):
        if fields is not None:
            self.fields = fields
        else:
            cols, rows = size
            self.fields = [[None for _ in range(rows)] for _ in range(cols)]

        super().__init__(current_player, other_player)

    def get_moves(self) -> Iterable[ConnectFourMove]:
        return [ConnectFourMove(i) for i, column in enumerate(self.fields) if column[-1] is None]

    def get_current_player(self) -> Player:
        return self._current_player

    def make_move(self, move: ConnectFourMove) -> 'ConnectFourState':
        new_fields = [list(column) for column in self.fields]
        self._put(new_fields, move)
        return ConnectFourState(current_player=self._other_player, other_player=self._current_player, fields=new_fields)

    def is_finished(self) -> bool:
        return self.get_winner() is not None

    def get_winner(self) -> Optional[Player]:
        for column_id in range(len(self.fields)):  # verticals
            for start_row_id in range(len(self.fields[column_id]) - 3):
                winner = self._check_four((column_id, start_row_id), (0, 1))
                if winner:
                    return winner
        
        for start_column_id in range(len(self.fields) - 3):  # horizontals
            for row_id in range(len(self.fields[start_column_id])):
                winner = self._check_four((start_column_id, row_id), (1, 0))
                if winner:
                    return winner

        for start_column_id in range(len(self.fields) - 3):  # diagonals
            for start_row_id in range(len(self.fields[start_column_id]) - 3):
                winner =\
                    self._check_four((start_column_id, start_row_id), (1, 1))\
                    or self._check_four((start_column_id, start_row_id + 3), (1, -1))
                if winner:
                    return winner

        return None
    
    def get_score(self,pMax):
        score = 0
        rows = len(self.fields[0])
        columns = len(self.fields)
        p1 = self.get_players()[0]
        p2 = self.get_players()[1]
        
        #Counting the score for the horizontal positions
        for row in range(rows):
            for col in range(columns-3):
                checkBox = [self.fields[col][row],self.fields[col+1][row],self.fields[col+2][row],self.fields[col+3][row]]
                p1Count = 0
                p2Count = 0
                empCount = 0
                
                for i in range(len(checkBox)):
                    if checkBox[i] == p1:
                        p1Count+=1
                    elif checkBox[i] == p2:
                        p2Count+=1
                    elif checkBox[i] == None:
                        empCount+=1
                if pMax==p1:
                    currentPlayerCount = p1Count
                    opponentPlayerCount = p2Count
                else:
                    currentPlayerCount = p2Count
                    opponentPlayerCount = p1Count
                    '''
                if self._current_player==p1:
                    currentPlayerCount = p2Count
                    opponentPlayerCount = p1Count
                elif self._current_player==p2:
                    currentPlayerCount = p1Count
                    opponentPlayerCount = p2Count'''
                '''
                currentPlayerCount = p1Count
                opponentPlayerCount = p2Count
                '''
                if currentPlayerCount == 4:
                    score=1000000
                elif currentPlayerCount == 3 and empCount==1:
                    score+=100
                elif currentPlayerCount == 2 and empCount==2:
                    score+=10
                elif opponentPlayerCount == 4:
                    score=-1000000
                elif opponentPlayerCount == 3 and empCount==1:
                    score+= -1000
                    
        #Couting the score for the vertical positions
        for col in range(columns):
            for row in range(rows-3):
                checkBox = self.fields[col][row:row+4]
                p1Count = 0
                p2Count = 0
                empCount = 0
                for i in range(len(checkBox)):
                    if checkBox[i] == p1:
                        p1Count+=1
                    elif checkBox[i] == p2:
                        p2Count+=1
                    elif checkBox[i] == None:
                        empCount+=1
                
                
                if pMax==p1:
                    currentPlayerCount = p1Count
                    opponentPlayerCount = p2Count
                else:
                    currentPlayerCount = p2Count
                    opponentPlayerCount = p1Count
                    '''
                if self._current_player==p1:
                    currentPlayerCount = p2Count
                    opponentPlayerCount = p1Count
                elif self._current_player==p2:
                    currentPlayerCount = p1Count
                    opponentPlayerCount = p2Count'''
                '''
                currentPlayerCount = p1Count
                opponentPlayerCount = p2Count
                '''
                if currentPlayerCount == 4:
                    score=1000000
                elif currentPlayerCount == 3 and empCount==1:
                    score+=100
                elif currentPlayerCount == 2 and empCount==2:
                    score+=10
                elif opponentPlayerCount == 4:
                    score=-1000000
                elif opponentPlayerCount == 3 and empCount==1:
                    score+= -1000
        
        #Counting tilted to the right slant positions
        for row in range(rows-3):
            for col in range(columns-3):
                checkBox = [self.fields[col][row],self.fields[col+1][row+1],self.fields[col+2][row+2],self.fields[col+3][row+3]]
                p1Count = 0
                p2Count = 0
                empCount = 0
                for i in range(len(checkBox)):
                    if checkBox[i] == p1:
                        p1Count+=1
                    elif checkBox[i] == p2:
                        p2Count+=1
                    elif checkBox[i] == None:
                        empCount+=1
                
                
                if pMax==p1:
                    currentPlayerCount = p1Count
                    opponentPlayerCount = p2Count
                else:
                    currentPlayerCount = p2Count
                    opponentPlayerCount = p1Count
                    '''
                if self._current_player==p1:
                    currentPlayerCount = p2Count
                    opponentPlayerCount = p1Count
                elif self._current_player==p2:
                    currentPlayerCount = p1Count
                    opponentPlayerCount = p2Count'''
                '''
                currentPlayerCount = p1Count
                opponentPlayerCount = p2Count
                '''
                if currentPlayerCount == 4:
                    score=1000000
                elif currentPlayerCount == 3 and empCount==1:
                    score+=100
                elif currentPlayerCount == 2 and empCount==2:
                    score+=10
                elif opponentPlayerCount == 4:
                    score=-1000000
                elif opponentPlayerCount == 3 and empCount==1:
                    score+= -1000
        
        #Counting tilted to the left slant positions
        for row in range(rows-3):
            for col in range(columns-3):
                checkBox = [self.fields[columns-1-col][rows-1-row],self.fields[columns-1-col-1][rows-1-row-1],self.fields[columns-1-col-2][rows-1-row-2],self.fields[columns-1-col-3][rows-1-row-3]]
                
                p1Count = 0
                p2Count = 0
                empCount = 0
                for i in range(len(checkBox)):
                    if checkBox[i] == p1:
                        p1Count+=1
                    elif checkBox[i] == p2:
                        p2Count+=1
                    elif checkBox[i] == None:
                        empCount+=1
                
                
                if pMax==p1:
                    currentPlayerCount = p1Count
                    opponentPlayerCount = p2Count
                else:
                    currentPlayerCount = p2Count
                    opponentPlayerCount = p1Count
                    '''
                if self._current_player==p1:
                    currentPlayerCount = p2Count
                    opponentPlayerCount = p1Count
                elif self._current_player==p2:
                    currentPlayerCount = p1Count
                    opponentPlayerCount = p2Count'''
                '''
                currentPlayerCount = p1Count
                opponentPlayerCount = p2Count
                '''
                if currentPlayerCount == 4:
                    score=1000000
                elif currentPlayerCount == 3 and empCount==1:
                    score+=100
                elif currentPlayerCount == 2 and empCount==2:
                    score+=10
                elif opponentPlayerCount == 4:
                    score=-1000000
                elif opponentPlayerCount == 3 and empCount==1:
                    score+= -1000
        
        return score
                
    def __str__(self) -> str:
        transposed = zip(*self.fields)
        text = '\n'.join(
            reversed([''.join(f'[{" " if field is None else field.char}]' for field in row) for row in transposed])
        )
        
        return f'Current player: {self._current_player.char}\n{text}'

    # below are helper methods for the public interface

    def _put(self, fields: List[List[Player]], move: ConnectFourMove) -> None:
        for i, field in enumerate(fields[move.column]):
            if field is None:
                fields[move.column][i] = self._current_player
                break

    def _check_four(self, start_coords: Tuple[int, int], move_coords: Tuple[int, int]) -> Optional[Player]:
        fields = {
            self.fields[start_coords[0] + move_coords[0] * i][start_coords[1] + move_coords[1] * i] for i in range(4)
        }

        if len(fields) != 1:
            return None

        return next(iter(fields))
