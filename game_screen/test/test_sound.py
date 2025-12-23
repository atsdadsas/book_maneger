import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from confing import BGM_LIST,SCREEN_WIDTH, SCREEN_HEIGHT, INITIAL_STRENGTH, MAX_VALUE, ALL_IMAGE_PATHS, IMAGE_STRENGTH_VALUES, IMAGE_EXHIBIT_SCALE,WHITE, GRAY, GREEN, RED, BLACK, BAR_WIDTH, BAR_HEIGHT, BAR_MARGIN, START_Y

pygame.init()
try:
    confing_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    bgm_path_relative = BGM_LIST[0] 
    bgm_path_absolute = os.path.normpath(os.path.join(confing_dir, bgm_path_relative))
    pygame.mixer.music.load(bgm_path_absolute)
    print("成功")
finally:
    print("失敗")


# print(f"{WHITE}")