from PIL import Image

#consts we will be using for readability
X = 0
Y = 1

W = 0
H = 1

R = 0
G = 1
B = 2

#config class for empirical values
class CONFIG:
    #configuratiile sunt pentru main monitor la rezolutia 1920 X 1080
    #jocul trebuie sa fie pornit si full screen la zoom 0 in browser pe monitorul principal
    SCREEN_PADDING              = (583,129) #x_pad_screen #y_pad_screen
    SCREEN_SIZE                 = (755, 603)
    PICTURE_SIZE                = (82, 56) #pic_sizex , pic_sizey
    SCREEN_GAME_BOARD_OFFSETS   = (88, 518) # offset_x ,offset_y_jos

    MOUSE_OFFSETS_IDLE          = (10, 10)
    MOUSE_OFFSETS_IDLE2         = (50,55)
    MOUSE_OFFSETS_IDLE3         = (30,39)

    GAME_BOARD_SIZE             = (7 , 9)
    EAR_COORDS                  =  (61,8)         #used to differentiate laser bears
    DIFFERENTIATE_COORDS        = [(40,6),(40,36)]
    #idx in vector for special pieces
    IDX_BROWN   = 5
    IDX_LASER   = 6
    IDX_BOOM    = 7


    TEMPLATE_IMAGES= [Image.open("template_img/albastru.png"),
                      Image.open("template_img/rosu.png"),
                      Image.open("template_img/verde.png"),
                      Image.open("template_img/galben.png"),
                      Image.open("template_img/roz.png"),
                      Image.open("template_img/brown.png"),
                      Image.open("template_img/laser.png"),
                      Image.open("template_img/colorbomb.png")]

    TEMPLATE_NAMES= ["albastru",
                     "rosu",
                     "verde",
                     "galben",
                     "roz",
                     "maro",
                     "laser",
                     "colorbomb"]

    EMPIRICAL_CLASSIFICATION_DISTANCE = 1000.0
    ANIMATION_PIXEL_THRESHOLD = 30000




