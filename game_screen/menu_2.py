import pygame
import sys
import numpy as np
import cv2
from confing_text import dialogue
from confing_mv import VideoManager
# ======================================================================
# 🚨 仮のconfingファイル定義 (実際のファイルの内容に置き換えてください)
# ======================================================================
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# ダミー ImageManager クラス
class ImageManager:
    def __init__(self, path):
        # 実際には画像をロードするが、ここではダミー
        self.surface = pygame.Surface((200, 300))
        self.surface.fill((100, 100, 100)) # 仮の色
    
    def draw(self, screen, *args):
        # 描画処理は省略し、とりあえず適当な位置に描画
        screen.blit(self.surface, (900, 450))

# ダミー VideoPlayer クラスと create_video_player 関数
class DummyVideoPlayer:
    def __init__(self, w, h, scale, path):
        self.video_surface = pygame.Surface((w, h))
        self.video_surface.fill((50, 50, 150)) # 仮の色
        self.current_frame = 0
        
    def update_video_frame(self):
        # フレーム更新処理のダミー
        self.current_frame += 1
        
    def draw_video(self, screen):
        # 動画背景のダミー描画
        screen.blit(self.video_surface, (0, 0))

def create_video_player(*args):
    return DummyVideoPlayer(*args)

# ======================================================================
from confing import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from confing_mv import create_video_player
from confing_im import ImageManager # ImageManager のインポートは上記仮定義に依存


class MOVieStart:
    VIDEO_PATH = '../file/5.avi'

    def __init__(self):
        pygame.init()

        try:
            self.font = pygame.font.SysFont("Meiryo", 36)
        except:
            self.font = pygame.font.Font(None, 36)
        self.video_player=0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dialogue Scene")

        self.running = True
        self.clock = pygame.time.Clock()
        self.cnt = 0

        self.current_name = ""
        self.current_text = ""
        self.name_surface = self.font.render("", True, WHITE)
        self.text_surfaces = [] # 🌟 修正: 複数行に対応するためのリスト
        self.x_left = 300
        self.answer = None

        self.images = [
            ImageManager("../file/girl1.png",0.1),
            ImageManager("../file/girl2.png",0.1),
            ImageManager("../file/girl3.png",0.1),
            ImageManager("../file/girl3.png",0.1)
        ]
        self.boss_images = [
            ImageManager("../file/new_boss1.png",0.2),
            ImageManager("../file/new_boss2.png",0.2)
        ]
        # -------------------- 🎬 動画関連 --------------------
        self.exhibit_player = 0.1
        self.background_video_manager = create_video_player(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.exhibit_player,
            self.VIDEO_PATH,
            x_pos=None,
            y_pos=None,
            position_x="left",
            position_y="bottom"
        )
        self.event_video_manager = None # Initialize event video manager
        # ------------------------------------------------------

    def update_text(self):
        """現在の会話データを更新"""
        if self.cnt < len(dialogue):
            line = dialogue[self.cnt]
            self.current_name = line["name"]
            # 呼び出し元のコード内で
            current_line = dialogue[self.cnt - 1] # リストから辞書を取り出す
            if current_line['id'] == 4:           # 取り出した辞書のキーにアクセス
                print(f"{self.cnt}")
                self.event_video_manager = VideoManager(
                screen_width=SCREEN_WIDTH,      # confingからインポートした定数を使用
                screen_height=SCREEN_HEIGHT,    # confingからインポートした定数を使用
                video_path="../file/2.avi",
                exhibit_scale=0.6,
                x_pos=None,
                y_pos=(SCREEN_HEIGHT/2)-300,
                position_x='center',
                position_y='NONE',
                )
            else:
                if self.event_video_manager:
                    self.event_video_manager = None # Clear event video if not id 4
                
            
            # 🌟 修正: \n で文字列を分割し、それぞれの行をSurfaceに変換
            self.current_text = line["text"]
            lines = self.current_text.split('\n') 
            
            self.name_surface = self.font.render(self.current_name, True, WHITE)
            # 複数行のSurfaceをリストとして保持
            self.text_surfaces = [self.font.render(text_line, True, WHITE) for text_line in lines]

            self.cnt += 1
        else:
            self.running = False  # 会話終了

    def display_text(self):
        """会話を表示"""
        self.update_text() # メインループに入る前に最初のセリフをロード

        # -------------MAIN-------------------------------------------------------------
        while self.running:
            # 現在表示中のセリフのインデックスを取得 (0 から len-1 の範囲)
            current_dialogue_index = self.cnt - 1 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # 🌟 修正点: MOUSEBUTTONDOWN のスペルミス修正と左クリック判定
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if current_dialogue_index >= 0:
                        current_dialogue_id = dialogue[current_dialogue_index]["id"]
                        if current_dialogue_id ==10: # Check if boss images are active
                            img1 = self.boss_images[0]
                            img2 = self.boss_images[1]
                            total_width = img1.width + img2.width + 50
                            start_x = (SCREEN_WIDTH - total_width) // 2
                            y_pos = SCREEN_HEIGHT - img1.height - 100

                            rect1 = pygame.Rect(start_x, y_pos, img1.width, img1.height)
                            rect2 = pygame.Rect(start_x + img1.width + 50, y_pos, img2.width, img2.height)

                            if rect1.collidepoint(event.pos):
                                print("Boss image 1 clicked!")
                                self.answer = 1
                                self.update_text() # Immediately advance dialogue
                            elif rect2.collidepoint(event.pos):
                                print("Boss image 2 clicked!")
                                self.answer = 2
                                self.update_text() # Immediately advance dialogue
                        else:
                            # クリックで次のセリフへ
                            if self.cnt < len(dialogue):
                                self.update_text()
                            else:
                                self.running = False
            # 🎥 動画更新
            if self.background_video_manager:
                self.background_video_manager.update_video_frame()
            if self.event_video_manager:
                self.event_video_manager.update_video_frame()

            # 背景を黒で塗りつぶし
            self.screen.fill(BLACK)

            # 🎬 動画を描画
            if self.background_video_manager:
                self.background_video_manager.draw_video(self.screen)
            if self.event_video_manager:
                self.event_video_manager.draw_video(self.screen)

            # 💬 名前を描画
            name_rect = self.name_surface.get_rect(left=100 + self.x_left, bottom=SCREEN_HEIGHT - 250)
            self.screen.blit(self.name_surface, name_rect)

            # 💬 セリフを描画 (複数行対応)
            y_position = SCREEN_HEIGHT - 200 # 最初の行の開始Y座標
            line_spacing = self.font.get_linesize() # フォントの行の高さ

            for surface in self.text_surfaces:
                text_rect = surface.get_rect(left=300 + self.x_left, top=y_position) # bottom から top に変更し、下に向かって描画
                self.screen.blit(surface, text_rect)
                y_position += line_spacing # 次の行のためにY座標を下にずらす

            # 画像描画
            if current_dialogue_index >= 0:
                current_dialogue_id = dialogue[current_dialogue_index]["id"] # Get the actual dialogue ID
                event_id = dialogue[current_dialogue_index]["event"]

                if current_dialogue_id == 10:
                    # 2つのボス画像を等間隔に配置
                    img1 = self.boss_images[0]
                    img2 = self.boss_images[1]

                    # 画像の幅と間隔を考慮して中央揃え
                    total_width = img1.width + img2.width + 50 # 50pxの間隔
                    start_x = (SCREEN_WIDTH - total_width) // 2
                    y_pos = SCREEN_HEIGHT - img1.height - 100 # 画面下部から100px上に配置

                    # 1つ目の画像 (左側)
                    img1.draw(self.screen, "left", "top", start_x, y_pos-300)
                    # 2つ目の画像 (右側)
                    img2.draw(self.screen, "left", "top", start_x + img1.width + 50, y_pos-300)

                elif 1 <= event_id <= 4:
                    if current_dialogue_id == 4: # If it's dialogue ID 4
                        # 右下に配置
                        self.images[event_id - 1].draw(self.screen, "right", "bottom", 0, 0)
                    else:
                        # それ以外の画像は右下に配置
                        self.images[event_id - 1].draw(self.screen, "right", "bottom", 0, 0)

            pygame.display.flip()
            self.clock.tick(30)

        # 終了処理
        return (self.answer, "practice") 
