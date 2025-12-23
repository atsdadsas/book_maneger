import pygame
import cv2
import numpy as np
import sys
# confing からのインポートはそのまま

# 外部から呼び出すための動画属性管理用のクラス
class VideoManager:
    """動画の読み込み、設定、フレーム処理を管理するクラス"""
    
    # 🌟 修正: 引数のデフォルト値を設定し、position の宣言を削除
    def __init__(self, screen_width, screen_height, exhibit_scale, video_path,
        x_pos=None, y_pos=None, position_x='left', position_y='top',
        target_width=None, target_height=None, y_offset=0):
        self.cap = None 
        self.video_surface = None
        self.video_rect = None
        self.frame_duration = 0
        self.last_frame_time = 0
        
        # 引数
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.exhibit_scale = exhibit_scale
        
        # 数値による直接指定
        self.x_pos = x_pos
        self.y_pos = y_pos
        
        # 文字列による配置指定 (小文字に変換)
        self.position_x = position_x.lower()
        self.position_y = position_y.lower()

        self.target_width = target_width
        self.target_height = target_height
        self.setup_video_assets(video_path)

    def setup_video_assets(self, video_path):
        """動画を開き、サイズと位置を設定する"""
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            print(f"エラー: 動画ファイル {video_path} を開けませんでした。")
            self.cap = None
            return

        # 1. サイズとリサイズ計算
        if self.target_width is not None and self.target_height is not None:
            new_width = self.target_width
            new_height = self.target_height
        else:
            original_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            original_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # 以前のコードで使用されていた exhibit_player の値（0.1）を再現
            new_width = int(original_width * self.exhibit_scale) 
            new_height = int(original_height * self.exhibit_scale) 
            
        # 2. 位置設定 (🌟 修正ロジックを適用)
        self.video_rect = pygame.Rect(0, 0, new_width, new_height)
        
        # --- X座標の設定 ---
        if self.x_pos is not None:
            # 数値 (x_pos) が指定されていれば優先
            self.video_rect.x = self.x_pos
        elif self.position_x == 'right':
            # 右寄せ
            self.video_rect.right = self.screen_width
        elif self.position_x == 'center':
            # X軸中央
            self.video_rect.centerx = self.screen_width // 2
        elif self.position_x == 'left':
            # 左寄せ（デフォルト）
            self.video_rect.left = 0 # 既存の 30px ではなく 0 をデフォルトとしました (必要に応じて 30 に変更してください)

        # --- Y座標の設定 ---
        if self.y_pos is not None:
            # 数値 (y_pos) が指定されていれば優先
            self.video_rect.y = self.y_pos
        elif self.position_y == 'bottom':
            # 下寄せ
            self.video_rect.bottom = self.screen_height
        elif self.position_y == 'center':
            # Y軸中央
            self.video_rect.centery = self.screen_height // 2
        elif self.position_y == 'top':
            # 上寄せ（デフォルト）
            self.video_rect.top = 0 # 既存の bottom-40 ではなく 0 をデフォルトとしました (必要に応じて self.screen_height - 40 に変更してください)

        # 3. フレームレートの設定 (変更なし)
        video_fps = self.cap.get(cv2.CAP_PROP_FPS)
        if video_fps == 0:
            video_fps = 30 
        self.frame_duration = 1000 / video_fps * 0.5
        self.last_frame_time = pygame.time.get_ticks()
        
        # 初回フレームを読み込む
        self.update_video_frame(initial_load=True)

    def update_video_frame(self, initial_load=False):
        """動画フレームを更新し、self.video_surface を新しいフレームで置き換える"""
        # ... (変更なし) ...
        if not self.cap:
            return

        current_time = pygame.time.get_ticks()
        if not initial_load and current_time - self.last_frame_time < self.frame_duration:
            return
            
        self.last_frame_time = current_time

        ret, frame = self.cap.read()
        
        if ret:
            # 1. BGR -> RGB 変換
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            
            # 2. NumPy配列の軸を転置: (高さ, 幅, 色) -> (幅, 高さ, 色)
            frame = frame.transpose([1, 0, 2])
            
            # 3. Surfaceへの変換
            frame_surface = pygame.surfarray.make_surface(frame)
            
            # 4. リサイズと格納
            resized_surface = pygame.transform.scale(frame_surface, (self.video_rect.width, self.video_rect.height))
            self.video_surface = resized_surface
        else:
            # 終端に達したらループ（巻き戻し）
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.update_video_frame(initial_load=True)

    def draw_video(self, screen):
        """メインループから呼び出され、動画を画面に blit する"""
        if self.video_surface and self.video_rect:
            screen.blit(self.video_surface, self.video_rect)

# ----------------------------------------------------------------------------------
# メインファイル (MainGameScene など) で使用する際の関数
def create_video_player(screen_width, screen_height, exhibit_scale, video_path, 
                        x_pos=None, y_pos=None, position_x='left', position_y='top'):
    """メインプログラムから VideoManager インスタンスを作成するための関数"""
    return VideoManager(screen_width, screen_height, exhibit_scale, video_path, 
                        x_pos, y_pos, position_x, position_y)