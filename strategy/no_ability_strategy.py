from strategy import Strategy
from config import *
from copy import deepcopy
from bot_utils import DebugUtils

class NoAbilityStrategy(Strategy):

    def __check_point(self,coords, rand, boardcpy):
        elementi, elementj = coords
        stack = boardcpy[elementi][elementj:]
        for el in stack:
            boardcpy[rand].append(el)

        boardcpy[elementi] = boardcpy[elementi][:elementj]
        return boardcpy

    def solve(self,board):
        best_move = (-1, 0, 0,0)

        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                #brown cannot be moved
                for k in range(j,len(board[i])):
                    if board[i][k] is CONFIG.IDX_BROWN:
                        break
                else:
                    for row in range(0, CONFIG.GAME_BOARD_SIZE[X]):
                        if row == i:
                            continue

                        if(len(board[row]) < 9):
                            board2 = self.__check_point((i, j), row, deepcopy(board[:]))
                            score = self._eval_board(board2[:])
                            if score > best_move[0]:
                                best_move = (score, i, j ,row)


                        #MyDebugUtils.PrintBoardImage(board2, "Debug\{0}_{1}_{2}.png".format(i, j, row))
        return best_move