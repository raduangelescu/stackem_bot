import os
import time
import win32api
import bot_utils
from PIL import Image
from PIL import ImageGrab
from config import *
from strategy.laser_ability_strategy import LaserAbilityStrategy
from strategy.no_ability_strategy import NoAbilityStrategy
from strategy.color_blast_ability_strategy import ColorBlastAbilityStrategy
from mouse_utils import MouseUtils
from sci_recognition import Reco

#BOT PYTHON Super Stack'em
class BotApplication:

    def __init__(self):
        self.utils = bot_utils.DebugUtils()
        self.browns_affected = []
        self.board = []
        self.reco = Reco()
        #Grab and crop the Game area
        self.box = (CONFIG.SCREEN_PADDING[X]+1, CONFIG.SCREEN_PADDING[Y]+1,
                    CONFIG.SCREEN_PADDING[X] + CONFIG.SCREEN_SIZE[W], CONFIG.SCREEN_PADDING[Y] + CONFIG.SCREEN_SIZE[H])

        self.strategies = []
        self.strategies.append(LaserAbilityStrategy("LaserAbilityStrategy"))
        self.strategies.append(NoAbilityStrategy("NoAbilityStrategy"))
        self.strategies.append(ColorBlastAbilityStrategy("ColorBlastAbilityStrategy"))

        self.im_end = Image.open(os.getcwd() + '\\testEndGame.png')

        self.reco.train()
        self.utils.get_characteristics()


    def can_start_move(self, image1, image2):
        count = 0
        pixels1 = image1.load()
        pixels2 = image2.load()
        min_x, min_y, max_x, max_y = -1, -1, -1, -1

        if len(self.browns_affected) > 0:
            ## Get the browns bounding box

            min_x = CONFIG.SCREEN_GAME_BOARD_OFFSETS[X] + min(self.browns_affected, key=lambda t: t[0])[X] * CONFIG.PICTURE_SIZE[X]
            max_y = CONFIG.SCREEN_SIZE[H]
            max_x = CONFIG.SCREEN_GAME_BOARD_OFFSETS[X] + (max(self.browns_affected, key=lambda t: t[0])[X] +1) * CONFIG.PICTURE_SIZE[X]
            min_y = CONFIG.SCREEN_GAME_BOARD_OFFSETS[Y] + min(self.browns_affected, key=lambda t: t[1])[Y] * CONFIG.PICTURE_SIZE[Y]

        for i in xrange(image1.size[0]):
            for j in xrange(image1.size[1]):
                # Do not take into account pixel differences in the brown pieces animation
                if min_x < i < max_x and min_y < j < max_y:
                    continue

                other_pixel = pixels2[i, j]

                if pixels1[i, j] != other_pixel:
                    count += 1

        return count < CONFIG.ANIMATION_PIXEL_THRESHOLD

    def do_recognition(self):
        self.board = []
        self.browns_affected = []
        win32api.SetCursorPos((CONFIG.SCREEN_PADDING[W] + CONFIG.MOUSE_OFFSETS_IDLE[X],
                               CONFIG.SCREEN_PADDING[H] - CONFIG.MOUSE_OFFSETS_IDLE[Y]))

        screen_shot = ImageGrab.grab(self.box)
        screen_shot.save("real.png",'PNG')

        for x in xrange(0, CONFIG.GAME_BOARD_SIZE[W]):

            new_row = []

            for y in xrange(0, CONFIG.GAME_BOARD_SIZE[H]):

                #1. Cut the tile
                tile = self.utils.get_tile_from_image(screen_shot, x, y)
                #2. Classify the tile
                class_id = self.reco.predict(tile)

                if class_id != -1:
                    ####print "({0},{1}) --> {2}".format(x, y, CONFIG.TEMPLATE_NAMES[class_id])
                    new_row.append(class_id)
                    if class_id == CONFIG.IDX_BROWN:
                        self.browns_affected.append((x, y))
                ####else:
                    ####print "({0},{1}) --> NIMIC".format(x, y)

            self.board.append(new_row)
        self.utils.print_board_image(self.board, "reco.png")

    def do_step(self):
        solutions = []

        for strategy in self.strategies:
            solution = strategy.solve(self.board)
            solutions.append(solution)
            print "Solutia data de strategia {0} are scorul {1} este Start ({2},{3}) End {4} ".\
                format(strategy.name, solution[0], solution[1], solution[2], solution[3])

        solutions = sorted(solutions, reverse=True)
        best_move = solutions[0]

        print "Solutia finala cu scorul {0} si mutarea Start ({1},{2}) End {3}".\
            format(best_move[0], best_move[1], best_move[2], best_move[3])

        MouseUtils.doMove(best_move, (len(self.board[best_move[3]])))


    def run(self):

        prev_img = ImageGrab.grab(self.box)

        while True:

            MouseUtils.random_idle_mouse_movement()
            time.sleep(0.5)
            MouseUtils.random_idle_mouse_movement()

            img = ImageGrab.grab()
            img = img.crop(self.box)

            self.do_recognition()

            if self.can_start_move(img, prev_img):

                if self.can_start_move(img, self.im_end):
                    break

                self.do_step()

            prev_img = img


if __name__ == '__main__':
    app = BotApplication()
    app.run()