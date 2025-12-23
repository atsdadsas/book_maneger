# 計算量o(n^2)
import pygame
import sys
import time

pygame.init()
SCREEN_W=1000
SCREEN_H=1000
TILE_SIZE=10
BLACK = (0, 0, 0)      # 背景
WHITE = (255, 255, 255) # 通路 (0)
RED = (255, 0, 0)      # ゴール (1)
GRAY = (100, 100, 100)  # 壁・探索済み (2)
BLUE = (0, 0, 255)     # 今調べている場所

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
maze = [
    [2, 2, 2, 2, 2],
    [2, 0, 0, 0, 2], # (1, 3) がゴール
    [2, 0, 2, 2, 2],
    [2, 0, 0, 1, 2],
    [2, 2, 2, 2, 2]
]
pos=[[1,1,0]]
while len(pos)>0:
    x,y,depth=pos.pop(0)
    
    if maze[x][y]==1:
        print(depth)
        break
    maze[x][y]=2
    if maze[x-1][y]<2:
        pos.append([x-1,y,depth+1])
    if maze[x+1][y]<2:
        pos.append([x+1,y,depth+1])
    if maze[x][y-1]<2:
        pos.append([x,y-1,depth+1])
    if maze[x][y+1]<2:
        pos.append([x,y+1,depth+1])
    # --- 描画処理 ---
    screen.fill(BLACK)
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            color = WHITE
            if maze[row][col] == 2: color = GRAY
            if maze[row][col] == 1: color = RED
            
            # 1マスを描画
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
    
    # 今調べている場所を青色で表示
    pygame.draw.rect(screen, BLUE, (y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
    pygame.display.flip()
    waiting = True
    time.sleep(0.3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 閉じるボタンが押されたら
            pygame.quit()
            sys.exit
    