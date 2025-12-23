import pygame
import sys
import cv2 
# confingの内容は仮定します
from confing import SCREEN_WIDTH, SCREEN_HEIGHT, INITIAL_STRENGTH, MAX_VALUE, ALL_IMAGE_PATHS, IMAGE_STRENGTH_VALUES, IMAGE_EXHIBIT_SCALE, WHITE,GRAY, GREEN, RED, BLACK, BAR_WIDTH, BAR_HEIGHT, BAR_MARGIN, START_Y
# ... (その他のconfingの定数は省略)
# VideoManager は confing_mv からインポートされていることを前提とします。
# 🚨 実際には VideoManager が定義されたファイルが必要です。
from confing_mv import VideoManager # <- この行はそのまま利用

class Start_Screen:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Meiryo", 36)
        self.text = self.font.render("エンタでスタート！", True, (252,252,252)) 
        self.running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("スタート画面")
        self.clock = pygame.time.Clock() # 実行速度を制御するためにクロックを追加

        # 🌟 修正1: VideoManagerを初期化時 (init) に一度だけ作成する
        self.video_player = VideoManager(
            screen_width=SCREEN_WIDTH,      # confingからインポートした定数を使用
            screen_height=SCREEN_HEIGHT,    # confingからインポートした定数を使用
            video_path="../file/6.gif",
            exhibit_scale=1.0 ,
            x_pos=None,
            y_pos=None,
            position_x="center",
            position_y="center",
        )

    def display_text(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.running = False
            
            # 🌟 修正2-A: 動画フレームを更新する
            self.video_player.update_video_frame() 
                
            self.screen.fill(BLACK)
            
            # 🌟 修正2-B: 動画フレームを描画する (背景が描かれた後、テキストの前に)
            self.video_player.draw_video(self.screen)
            text_rect=self.text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
            # テキストを描画 (動画の上に重ねて表示される)
            self.screen.blit(self.text, (text_rect))
            
            pygame.display.flip()
            self.clock.tick(60) # 速度を60FPSに制限
            
        # 🌟 修正3: ループ終了後、動画のリソースを解放する
        if self.video_player and self.video_player.cap: # <--- Add this check
            self.video_player.cap.release()
        return "menu_2"

if __name__ == "__main__":
    start_screen_instance = Start_Screen()
    start_screen_instance.display_text()