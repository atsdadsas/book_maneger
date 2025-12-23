import pygame

# --- 色の定義 ------------------
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
# --- SFCの値とゲージ設定 -----------------
INITIAL_STRENGTH = 1000
MAX_VALUE = 1000
BAR_WIDTH = 300
BAR_HEIGHT = 30
BAR_MARGIN = 50
START_Y = 150
LENGTH=3
# SCREEN_WIDTH = 1500
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1000

HARF_SCREEN_WIDTH=SCREEN_WIDTH/2
HARF_SCREEN_HEIGHT=SCREEN_WIDTH/2


FONT_SIZE_MAIN = 36

# # -------------羊の画像---------------------------------------
# ALL_IMAGE_PATHS = ["../file/sheep.png", "../file/sheep.png", "../file/sheep.png", "../file/sheep.png"]

# IMAGE_STRENGTH_VALUES = {
#     "../file/sheep.png": -100
# }

# IMAGE_EXHIBIT_SCALE = 0.2
    
# START_IMAGE_PATHS = ["../file/sheep.png", "../file/sheep.png"]

# --------------画像--------------------------------------------
ALL_IMAGE_PATHS = ["../file/card1.png", "../file/card2.png","../file/card3.png","../file/card4.png"]
IMAGE_STRENGTH_VALUES = {
    "../card1.png": -50,
    "../card2.png": -100,
    "../card3.png": -150,
    "../card4.png": -10 
}

IMAGE_EXHIBIT_SCALE=0.2
    
# ----START_-----------------------------------------
START_IMAGE_PATHS = ["../file/new_boss1.png","../file/new_boss2.png"]

# -----video--------------------------------------
wait_time=1

# -----bgm-----------------------------------
BGM_LIST=["../file/sound1.mp3"]