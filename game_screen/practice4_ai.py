import pygame
import sys
import os
import random
import numpy as np # 💡 動画再生のために追加
import cv2 # 💡 動画再生のために追加
from confing_mv import VideoManager # Import VideoManager
from confing_write_text import TextDisplayManager # Import TextDisplayManager
# confing.py からのインポートはそのまま利用
from confing import SCREEN_WIDTH, SCREEN_HEIGHT, INITIAL_STRENGTH, MAX_VALUE, ALL_IMAGE_PATHS, IMAGE_STRENGTH_VALUES, IMAGE_EXHIBIT_SCALE, GRAY, GREEN, RED, BLACK, BAR_WIDTH, BAR_HEIGHT, BAR_MARGIN, START_Y

pygame.init()

# 画面設定（confing.pyから取得）
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My pygame window")

# フレームレート制御用
clock = pygame.time.Clock()

class MainGameScene:
    # 💡 initial_path: 静止画ボス、video_path: 動画
    def __init__(self, initial_path=None, answer=None): # ◀️ 動画パスを削除
        self.answer = answer

        # 右側の動画パスを決定
        right_video_path = ''
        if self.answer == 1:
            right_video_path = '../file/7.avi'
        elif self.answer == 2:
            right_video_path = '../file/6.avi'
        else:
            right_video_path = '../file/5.avi' # デフォルト値またはエラーケース
        
        self.screen = screen
        self.running = True
        
        self.strength = INITIAL_STRENGTH
        self.max_value = MAX_VALUE
        self.exhibit = IMAGE_EXHIBIT_SCALE
        self.max_value1_player = 0.1
        self.exhibit_player = 0.1
        self.all_image_paths = ALL_IMAGE_PATHS
        self.IMAGE_STRENGTH_VALUES = IMAGE_STRENGTH_VALUES
        
        # 選択肢画像の初期化
        self.image_paths = random.sample(ALL_IMAGE_PATHS, 3)
        self.LENGTH = len(self.image_paths)
        self.resized_images = []
        self.my_image_rects = []
        self.new_image_size = (0, 0) # 選択肢画像のサイズ
        
        # 🌟 静止画ボス画像関連の属性 (右側表示用)
        self.start_image_path = initial_path
        self.loaded_boss_img = None
        self.boss_image = None
        self.boss_rect = None
        self.new_image_size_boss = (0, 0)
        
        # 🌟 動画再生関連の属性 (左側表示用)
        # 1つ目の動画の元のサイズを取得し、それを基準にリサイズ
        temp_cap = cv2.VideoCapture('../file/5.avi')
        if temp_cap.isOpened():
            original_width = int(temp_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            original_height = int(temp_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            temp_cap.release()
        else:
            print(f"警告: 1つ目の動画ファイル {video_path} を開けませんでした。デフォルトサイズを使用します。")
            original_width, original_height = 640, 480 # デフォルト値

        target_width = int(original_width * 0.1) # exhibit_scaleを直接使用
        target_height = int(original_height * 0.1) # exhibit_scaleを直接使用

        self.first_video_manager = VideoManager(
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
            exhibit_scale=0.1, # 適切なスケールを設定
            video_path='../file/5.avi', # 左側は常に5.avi
            x_pos=None,
            y_pos=None,
            position_x="left",
            position_y="bottom",
            target_width=target_width,
            target_height=target_height,
        )

        # 🌟 2つ目の動画 (7.avi) の設定 (右下表示用)
        self.second_video_manager = VideoManager(
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
            exhibit_scale=0.1, # 適切なスケールを設定
            video_path=right_video_path, # 右側の動画パス
            x_pos=None,
            y_pos=None,
            position_x="right",
            position_y="bottom",
            target_width=target_width,
            target_height=target_height,
        )
        # 🌟 初期設定を実行
        # self.setup_video_assets() # ◀️ 動画の設定 (VideoManagerが担当するため不要に)
        
        # 🌟 静止画ボス画像のロードとリサイズ・配置 (右側)
        if initial_path:
            try:
                self.loaded_boss_img = pygame.image.load(initial_path).convert_alpha()
                self.resize_and_position_boss()
            except pygame.error as e:
                print(f"Error loading boss image at {initial_path}: {e}")
        
        # 🌟 選択肢画像アセットの設定を実行
        self.setup_game_assets()

        # 🌟 TextDisplayManagerのインスタンスを作成
        self.text_manager = TextDisplayManager(self.screen)
        self.text_manager.update_text()

    # ----------------------静止画ボス画像関連----------------------------------
    def resize_and_position_boss(self):
        # ... (コードはそのまま) ...
        if not self.loaded_boss_img:
            return
            
        original_width, original_height = self.loaded_boss_img.get_size()
        new_height = int(original_height * self.exhibit)
        new_width = int(original_width * self.exhibit)
        self.new_image_size_boss = (new_width, new_height)
        
        self.boss_image = pygame.transform.scale(self.loaded_boss_img, self.new_image_size_boss)
        
        # 💡 右端から30px、下端から50pxに配置
        self.boss_rect = self.boss_image.get_rect(right=SCREEN_WIDTH - 30, bottom=SCREEN_HEIGHT-50)

    # 🌟 ボス画像の描画メソッド
    def boss_appear(self):
        if self.boss_image and self.boss_rect:
            self.screen.blit(self.boss_image, self.boss_rect)
            
    # ----------------------メインループの修正----------------------------------
    def main(self):
        while self.running:
                                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #  діалогを進める
                    if not self.text_manager.update_text():
                        # もしテキストが終了したら、何か他の処理を行う（例：ゲーム終了）
                        pass

                    # クリック処理は省略
                    for i, rect in enumerate(self.my_image_rects):
                        if rect.collidepoint(event.pos):
                            current_path = self.image_paths[i]
                            self.update_strength_by_image(current_path)
                            self.replace_image(i)
            # 🌟 動画フレームの更新をメインループに追加
            if self.first_video_manager:
                self.first_video_manager.update_video_frame()
            if self.second_video_manager:
                self.second_video_manager.update_video_frame()
            
            # --- 🌟 描画処理 -------------------------------
            self.screen.fill(BLACK) 
            self.gauge() # ゲージの描画
            if self.first_video_manager:
                self.first_video_manager.draw_video(self.screen) # 1つ目の動画の描画
            if self.second_video_manager:
                self.second_video_manager.draw_video(self.screen) # 2つ目の動画の描画
            self.boss_appear() # ◀️ 静止画ボスの描画 (右側)
            self.image_appear() # 選択肢となる画像の描画

            # テキストを描画
            self.text_manager.draw_text()
            
            pygame.display.flip()
            clock.tick(60)

    # 💡 選択肢画像の設定 (省略されていたメソッドを再掲)
    def setup_game_assets(self):
        x_offset = 50 + self.first_video_manager.video_rect.height
        image_gap = 50 
        
        for path in self.image_paths:
            try:
                img = pygame.image.load(path).convert_alpha()
            except pygame.error as e:
                print(f"Error loading image at {path}: {e}")
                sys.exit()

            if self.new_image_size == (0, 0):
                original_width, original_height = img.get_size()
                new_height = int(original_height * self.exhibit)
                new_width = int(original_width * self.exhibit)
                self.new_image_size = (new_width, new_height)
                
            resized_image = pygame.transform.scale(img, self.new_image_size)
            self.resized_images.append(resized_image)
            
            my_image_rect = resized_image.get_rect()
            my_image_rect.topleft = (x_offset, SCREEN_HEIGHT - self.new_image_size[1] - 500) 
            self.my_image_rects.append(my_image_rect)
            
            x_offset += self.new_image_size[0] + image_gap

    # 💡 選択肢画像の描画 (省略されていたメソッドを再掲)
    def image_appear(self):
        for i in range(self.LENGTH):
            self.screen.blit(self.resized_images[i], self.my_image_rects[i])

    # 💡 ゲージの描画 (省略されていたメソッドを再掲)
    def gauge(self):
        gauge_x = SCREEN_WIDTH - (BAR_WIDTH + 50) 
        pygame.draw.rect(self.screen, GRAY, (gauge_x, START_Y + BAR_MARGIN, BAR_WIDTH, BAR_HEIGHT), 2)
        fill_width = int((self.strength / self.max_value) * BAR_WIDTH)
        fill_color = RED if self.strength <= self.max_value * 0.25 else GREEN
        pygame.draw.rect(self.screen, fill_color, (gauge_x, START_Y + BAR_MARGIN, fill_width, BAR_HEIGHT))
        
    # 💡 Strength更新 (省略されていたメソッドを再掲)
    def update_strength_by_image(self, image_path):
        if image_path in self.IMAGE_STRENGTH_VALUES:
            self.strength += self.IMAGE_STRENGTH_VALUES[image_path]
            self.strength = max(0, min(self.strength, self.max_value))
        else:
            print(f"警告: {image_path} に対応する strength 値がありません。")
        print(f"現在の Strength: {self.strength}")

    # 💡 画像入れ替え (省略されていたメソッドを再掲)
    def replace_image(self, index):
        temp_paths = [path for path in self.all_image_paths if path not in self.image_paths]
        
        if temp_paths:
            new_path = random.choice(temp_paths)
            
            new_image_loaded = pygame.image.load(new_path).convert_alpha()
            resized_image = pygame.transform.scale(new_image_loaded, self.new_image_size)
            
            self.resized_images[index] = resized_image
            self.image_paths[index] = new_path
        else:
            print("警告: すべての画像が表示中です。入れ替え可能な画像がありません。")


if __name__ =="__main__":
    try:
        # 💡 静止画ボス画像と動画パスの両方を指定してインスタンス化する
        # 例: game = MainGameScene(initial_path="assets/static_boss.png") 
        game = MainGameScene() 
        game.main()
    except Exception as e:
        print(f"ゲーム実行中にエラーが発生しました: {e}")
    finally:
        pygame.quit()
        sys.exit()