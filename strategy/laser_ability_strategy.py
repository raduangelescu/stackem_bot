from strategy import Strategy
from config import *
from copy import deepcopy

class LaserAbilityStrategy(Strategy):

    def __check_count_vertical_blast(self, board):
        vx, vy = -1, -1

        for i, row in enumerate(board):
                ids = len(row) - 1
                if ids < 0:
                    continue

                if board[i][ids] is CONFIG.IDX_LASER:
                    #we found a vertical laser check score
                    vx, vy = i, ids

        max_count, max_x = 0, -1

        if vx is not -1 and vy is not -1:
            for i, row in enumerate(board):
                if len(row) < CONFIG.GAME_BOARD_SIZE[H]:
                    tmp_cpy = deepcopy(board)
                    tmp_cpy[i] = [-1] * len(row)
                    score = self._eval_board(tmp_cpy) + len(row) -1
                    if max_count < score:
                        max_count, max_x = score, i

        return max_count, vx, vy, max_x

    def solve(self, board):
        return self.__check_count_vertical_blast(board)