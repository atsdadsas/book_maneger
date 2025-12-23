import pygame
import sys
import os
import random
import time
from confing import BGM_LIST,FONT_SIZE_MAIN,SCREEN_WIDTH, SCREEN_HEIGHT, INITIAL_STRENGTH, MAX_VALUE, ALL_IMAGE_PATHS, IMAGE_STRENGTH_VALUES, IMAGE_EXHIBIT_SCALE, GRAY,WHITE, GREEN, RED, BLACK, BAR_WIDTH, BAR_HEIGHT, BAR_MARGIN, START_Y,START_IMAGE_PATHS

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Start_Game_Screen:
    def __init__(self,initial_path=None):
        #    これでクリック時に得られるパスと辞書のキーが一致します
        self.screen = screen
        self.running = True
        self.strength = INITIAL_STRENGTH
        self.max_value = MAX_VALUE
        self.all_image_paths = START_IMAGE_PATHS
        # 💡 属性名 self.image_strength_values に合わせる
        self.image_strength_values = IMAGE_STRENGTH_VALUES
        if isinstance(START_IMAGE_PATHS, str):
            self.image_paths = [START_IMAGE_PATHS]
        else:
            self.image_paths = list(START_IMAGE_PATHS)
        self.LENGTH = len(self.image_paths)
        self.exhibit = IMAGE_EXHIBIT_SCALE
        self.rect_to_draw = pygame.Rect(100, 100, 50, 50)
        self.is_visible = True
        self.resized_images = []
        self.my_image_rects = []
        self.images = [] 
        # 💡 定数 LENGTH ではなく self.LENGTH を使う
        self.is_image_visible = [True] * self.LENGTH
        self.new_image_size = (0, 0) # setup_game_assets内で計算し、mainで再利用するサイズ
        # 🌟 画像アセットの設定を実行
        self.setup_game_assets()
        self.font= pygame.font.SysFont("Meiryo", FONT_SIZE_MAIN) 
        self.text=self.font.render("アイコンをクリックしてスタート",True,WHITE)
        self.sound_1()
        self.sound_0()
        
    def setup_game_assets(self):
        x_offset=300
        for path in self.image_paths:
            img=pygame.image.load(path).convert_alpha()
            if self.new_image_size == (0, 0):
                original_width, original_height = img.get_size()
                new_height = int(original_height * self.exhibit)
                new_width = int(original_width * self.exhibit)
                self.new_image_size = (new_width, new_height)
                
            resized_image = pygame.transform.scale(img, self.new_image_size)
            self.resized_images.append(resized_image)
            
            # 3. Rect（位置情報）の配置
            my_image_rect = resized_image.get_rect()
            # 画面下部に配置する計算
            my_image_rect.topleft = (x_offset, SCREEN_HEIGHT - self.new_image_size[1] - 400) 
            self.my_image_rects.append(my_image_rect)
            x_offset += self.new_image_size[0] + 250 # 次の画像の位置
    def draw_text(self):
        # 画面中央上部に配置
        text_rect = self.text.get_rect(center=(SCREEN_WIDTH // 2, 800))
        self.screen.blit(self.text,text_rect)
        

    def run(self):
        self.running=True
        self.clicked_image_path = None
        while self.running:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    self.running=False
                if event.type== pygame.MOUSEBUTTONDOWN:
                    for i,rect in enumerate(self.my_image_rects):
                        if rect.collidepoint(event.pos):
                            path = self.image_paths[i]
                            self.clicked_image_path = path
                            self.running = False
                            print(f"画像がクリックされました: {path}")
                            if i==0:
                                self.sound_0()
                                pygame.mixer.music.play()
                                time.sleep(1.0)
                                break
                            elif i==1:
                                self.sound_1()
                                pygame.mixer.music.play()
                                time.sleep(1.0)
                                break
            screen.fill(BLACK)
            self.image_appear()
            self.draw_text()
            pygame.display.flip()
        return self.clicked_image_path 
    def sound_0(self):
                    try:
                        pygame.mixer.music.load("../file/sound0.mp3")
                        print("音声ダウンロード成功")
                    except:
                        print("音声をダウンロードできません")
    def sound_1(self):
                    try:
                        pygame.mixer.music.load("../file/sound1.mp3")
                        print("音声ダウンロード成功")
                    except:
                        print("音声をダウンロードできません")
        
    def image_appear(self):
        for i in range(self.LENGTH):
            if self.is_image_visible[i]:
                self.screen.blit(self.resized_images[i], self.my_image_rects[i])

if __name__ == "__main__":
    try:
        game = Start_Game_Screen() 
        game.run()
    except Exception as e:
        print(f"ゲーム実行中にエラーが発生しました: {e}")
    finally:
        pygame.quit()
        sys.exit()