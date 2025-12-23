import pygame
import sys

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
BLACK=(0,0,0)
WHITE=(255,255,255)

class AppConfig:

    def __init__(self):
        pygame.init()
        self.font=pygame.font.SysFont("Meiryo",36)
        self.running=True
        self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("Blit")
        self.text_surface=self.font.render("hello",True,WHITE)
        self.text_surface2=self.font.render("音量",True,WHITE)
        self.text_surface3=self.font.render("クレジット",True,WHITE)
        self.text_rect=self.text_surface.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        self.text_rect2=self.text_surface.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2+150))
        self.text_rect3=self.text_surface.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2-150))
        self.clock = pygame.time.Clock()
        
    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
                if event.type==pygame.MOUSEBUTTONDOWN:
                    mouse_x,mouse_y=event.pos
                    if self.text_rect.collidepoint(mouse_x,mouse_y):
                        print("hello")
                    elif self.text_rect2.collidepoint(mouse_x,mouse_y):
                        print("音量")
                    elif self.text_rect3.collidepoint(mouse_x,mouse_y):
                        print("クレジット")
                        
            self.screen.fill(BLACK)
            self.screen.blit(self.text_surface,self.text_rect)
            self.screen.blit(self.text_surface2,self.text_rect2)
            self.screen.blit(self.text_surface3,self.text_rect3)
            pygame.display.flip()
            
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__=="__main__":
    app=AppConfig()
    app.main()
