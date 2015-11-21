from config import *
import random
import win32api
import win32con
import time

class MouseUtils:

    # mouse control
    @staticmethod
    def drag(x, y, movx, movy):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.5)
        win32api.SetCursorPos((movx, movy))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(2.0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(1.0)
        win32api.SetCursorPos((movx,CONFIG.SCREEN_PADDING[Y]))

    @staticmethod
    def leftClick():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    @staticmethod
    def random_idle_mouse_movement():
        random_mouse_coord = (random.randint(CONFIG.MOUSE_OFFSETS_IDLE3[0], CONFIG.MOUSE_OFFSETS_IDLE3[1]),
                              random.randint(CONFIG.MOUSE_OFFSETS_IDLE2[0], CONFIG.MOUSE_OFFSETS_IDLE2[1]))

        win32api.SetCursorPos((CONFIG.SCREEN_PADDING[X]+ random_mouse_coord[X],
                               CONFIG.SCREEN_PADDING[Y]+ random_mouse_coord[Y]))
    @staticmethod
    def doMove(best_move,leny):
        xclick = CONFIG.SCREEN_PADDING[X]+1 + CONFIG.SCREEN_GAME_BOARD_OFFSETS[X] + best_move[1] * CONFIG.PICTURE_SIZE[X] + CONFIG.PICTURE_SIZE[X]/2.0
        yclick = CONFIG.SCREEN_PADDING[Y]+1 + CONFIG.SCREEN_GAME_BOARD_OFFSETS[Y] - (best_move[2]+1)* CONFIG.PICTURE_SIZE[Y] + CONFIG.PICTURE_SIZE[Y]/2.0

        xclickmove = CONFIG.SCREEN_PADDING[X] +1 + CONFIG.SCREEN_GAME_BOARD_OFFSETS[X] + best_move[3] * CONFIG.PICTURE_SIZE[X] + CONFIG.PICTURE_SIZE[X]/2.0
        yclickmove = CONFIG.SCREEN_PADDING[Y] +1 + CONFIG.SCREEN_GAME_BOARD_OFFSETS[Y] - leny         * CONFIG.PICTURE_SIZE[Y] - CONFIG.PICTURE_SIZE[Y]/2.0
        print xclickmove

        MouseUtils.drag(int(xclick), int(yclick), int(xclickmove), int(yclickmove))
        if(best_move[3] is  best_move[1]):
            MouseUtils.drag(int(xclickmove), int(yclickmove), int(xclickmove), int(yclickmove))