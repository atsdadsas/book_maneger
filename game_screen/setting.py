import pygame
import sys

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
BLACK=(0,0,0)
WHITE=(255,255,255)

class AppConfig:

    def __init__(self):
        pygame.init()
        self.font=pygame.font.SysFont(None,36)
        self.running=True
        self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("Blit")
        self.text_surface=self.font.render("hello",True,WHITE)
        self.text_rect=self.text_surface.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        
        self.clock = pygame.time.Clock()
        
    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
            self.screen.fill(BLACK)
            self.screen.blit(self.text_surface,self.text_rect)
            pygame.display.flip()
            
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
if __name__=="__main__":
    app=AppConfig()
    app.main