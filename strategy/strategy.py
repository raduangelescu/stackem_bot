from config import *
from copy import deepcopy
#solution needs to be a tuple of this form
# (score, first x click , first y click, second x click)
class Strategy:
    def __init__(self,name):
        self.name = name

    def solve(self, board):
        raise NotImplementedError("Subclass must implement abstract method")

    def _build_contracted_board(self, board):
        board_contract = []
        for row in board:
            if len(row) == 0:
                board_contract.append([])

        for row in board:
            new_row = []
            for el in row:
                new_row.append(el)
            board_contract.append(new_row)

        return board_contract

    def _eval_board(self, boardcpy):

        self.fill_with(boardcpy)
        board_contract = self._build_contracted_board(boardcpy)

        for i, row in enumerate(board_contract):
            for j, element in enumerate(row):
                if element is not -1:

                    temp_cpy = deepcopy(board_contract)
                    #fill exploded with -2
                    ffcount = self.floodFill(temp_cpy, i, j, -2)

                    if ffcount >= 3:
                        cpy_without_exploded = []
                        for row in temp_cpy:
                            row_exploded = [x for x in row if x != -2]
                            cpy_without_exploded.append(row_exploded)

                        temp_cpy = cpy_without_exploded
                        return ffcount + self._eval_board(temp_cpy)
        return 0

    def floodFill(self,boardcpy, x, y, color):

        width = len(boardcpy)
        height = len(boardcpy[0])

        oldNum = boardcpy[x][y]

        stiva = [(x, y)]
        while len(stiva) > 0:
            x, y = stiva.pop()

            if boardcpy[x][y] != oldNum:
                continue

            boardcpy[x][y] = color

            if x > 0:  # left
                stiva.append((x-1, y))

            if y > 0:  # up
                stiva.append((x, y-1))

            if x < width-1:  # right
                stiva.append((x+1, y))

            if y < height-1:  # down
                stiva.append((x, y+1))

        count = 0
        for el in boardcpy:
            for elz in el:
                if elz == color:
                    count += 1

        return count


    def fill_with(self,board):
        maxlen = 0
        for el in board:
            if maxlen < len(el):
                maxlen = len(el)
        for el in board:
            if len(el) < maxlen:
                for s in range(0, (maxlen - len(el))):
                    el.append(-1)
