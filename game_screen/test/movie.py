import pygame
import sys
import cv2
import numpy as np

pygame.init()
WHITE=(255,255,255)
BALCK=(0,0,0)
screen= pygame.display.set_mode((1000,1000))
movie_sample = cv2.VideoCapture("../2.avi")
wait_time=1
if not movie_sample.isOpened():
    print("動画を開けませんでした")
    sys.exit()


running=True
while running:
    
    for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                running=False
                
    ret, frame = movie_sample.read()
    if not ret:
        # 再生が終わったら終了
        break
    
    screen.fill(BALCK)
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    frame_surface = pygame.surfarray.make_surface(np.rot90(frame))
    
    screen.blit(frame_surface,(0,0))
    
    pygame.time.delay(wait_time)
    
    pygame.display.flip()

movie_sample.release()
pygame.quit()
sys.exit()