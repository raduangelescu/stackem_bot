from PIL import Image
from config import *

class DebugUtils:

    def __init__(self):

        self.background = Image.new("RGBA",(CONFIG.SCREEN_SIZE[W],CONFIG.SCREEN_SIZE[H]),(255,255,255,255))
        self.vector_characteristics = []

    @staticmethod
    def get_new_image_characteristics(img):
        refcolors = []
        for diff in CONFIG.DIFFERENTIATE_COORDS:
            pixel = img.getpixel((diff[0],diff[1]))
            cR = pixel[0]
            cG = pixel[1]
            cB = pixel[2]
            refcolors.append((cR,cB,cG))

        refcolors.append(img.getpixel(CONFIG.EAR_COORDS))

        return refcolors


    def get_characteristics(self):
        for img in CONFIG.TEMPLATE_IMAGES:
            refcolors = []
            for diff in CONFIG.DIFFERENTIATE_COORDS:
                pixel = img.getpixel((diff[0],diff[1]))
                cR = pixel[0]
                cG = pixel[1]
                cB = pixel[2]
                refcolors.append((cR,cB,cG))

            refcolors.append(img.getpixel(CONFIG.EAR_COORDS))
            self.vector_characteristics.append(refcolors)


    def classify_characteristic(self, newchar):
        c = -1
        mindist = 999999999
        minidx = -1


        for vc in self.vector_characteristics:
            c = c + 1
            dist = DebugUtils.get_characteristic_distances(newchar, vc)

            if((CONFIG.EMPIRICAL_CLASSIFICATION_DISTANCE    < dist[0] or  CONFIG.EMPIRICAL_CLASSIFICATION_DISTANCE  < dist[1] )and  dist[1] > 100 and dist[0] > 100 ):
                continue

            if(mindist > dist[0]):
                mindist = dist[0]
                minidx = c
            if(mindist > dist[1]):
                mindist = dist[1]
                minidx = c


        if minidx == CONFIG.IDX_LASER or minidx == CONFIG.IDX_BOOM:
            if self.color_distance(newchar[2],self.vector_characteristics[CONFIG.IDX_LASER][2])  < self.color_distance(newchar[2],self.vector_characteristics[CONFIG.IDX_BOOM][2]):
                minidx = CONFIG.IDX_LASER
            else:
                minidx = CONFIG.IDX_BOOM

        return minidx

    @staticmethod
    def get_tile_from_image(image, x , y):
        box_crop = (CONFIG.SCREEN_GAME_BOARD_OFFSETS[X] + x     * CONFIG.PICTURE_SIZE[X],  CONFIG.SCREEN_GAME_BOARD_OFFSETS[Y] - ((y+1)* CONFIG.PICTURE_SIZE[Y]),
                        CONFIG.SCREEN_GAME_BOARD_OFFSETS[X] +(x+1)  * CONFIG.PICTURE_SIZE[X],  CONFIG.SCREEN_GAME_BOARD_OFFSETS[Y]  -((y  )* CONFIG.PICTURE_SIZE[Y]))
        tile = image.copy().crop(box_crop)
        return tile


    @staticmethod
    def color_distance( c1, c2):
        return (c1[0] - c2[0]) * (c1[0] - c2[0]) + (c1[1] - c2[1]) * (c1[1] - c2[1]) + (c1[2] - c2[2]) * (c1[2] - c2[2])

    @staticmethod
    def get_characteristic_distances(vc,vc1):
        return (DebugUtils.color_distance(vc[0],vc1[0]),DebugUtils.color_distance(vc[1],vc1[1]))

    def __printImg(self,img,x,y):
        offset = (x,y)
        self.background.paste(img,offset)

    def print_board_image(self, evalboard, name):
        template_width,template_height = CONFIG.TEMPLATE_IMAGES[0].size
        for i in range (0, len(evalboard)):
            for j in range(len(evalboard[i])-1, -1, -1):
                if 0 <= evalboard[i][j] < len(CONFIG.TEMPLATE_IMAGES):
                    imgtoprint = CONFIG.TEMPLATE_IMAGES[evalboard[i][j]]
                    self.__printImg(imgtoprint, i*template_width, CONFIG.SCREEN_SIZE[H] - ((j + 1)*template_height))


        self.background.save(name+ ".png")

        self.background = Image.new("RGBA",(CONFIG.SCREEN_SIZE[W],CONFIG.SCREEN_SIZE[H]),(255,255,255,255))



