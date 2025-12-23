import pygame
import sys
import os

pygame.init()
screen =pygame.display.set_mode((1000,1000))
runnnig =True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # ウィンドウの閉じるボタンが押されたらループを終了
            running = False
    screen.fill((255,255,255))
    pygame.display.flip()
    pygame.quit()
    sys.exit()