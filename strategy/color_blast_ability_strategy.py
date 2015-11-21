from strategy import Strategy
from config import *
from copy import deepcopy

class ColorBlastAbilityStrategy(Strategy):

    def frequency_for_color(self,board_c,col):
        sum = 0
        for i in range(0, len(board_c)):
            for j in range(0, len(board_c[i])):
                if(board_c[i][j] == col):
                    sum = sum + 1
                    board_c[i][j] = -2

        return sum

    def __checkCountColorBlast(self,board):

        vx, vy = -1, -1
        for i, row in enumerate(board):
                ids = len(row) -1
                if ids < 0:
                    continue
                if row[ids] is CONFIG.IDX_BOOM:
                    #we found a boom laser check score
                    vx, vy = i, ids

        max_count, max_x = 0, -1

        if vx is not -1 and vy is not -1:
            for i, row in enumerate(board):
                if len(row) < 9:
                    ids = len(row)-1
                    boardcpy = deepcopy(board)
                    frec = self.frequency_for_color(boardcpy, boardcpy[i][ids])
                    score = self._eval_board(boardcpy) + frec
                    if(max_count < score ):
                        max_count = score
                        max_x = i

        return max_count,vx, vy, max_x

    def solve(self,board):
        return self.__checkCountColorBlast(board)