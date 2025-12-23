import pygame
from confing_text import dialogue
from confing import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from confing_mv import VideoManager

class TextDisplayManager:
    def __init__(self, screen, font_name="Meiryo", font_size=36, x_offset=300, y_offset_name=550, y_offset_text=600, name_color=WHITE, text_color=WHITE):
        self.screen = screen
        try:
            self.font = pygame.font.SysFont(font_name, font_size)
        except:
            self.font = pygame.font.Font(None, font_size)
        
        self.x_offset = x_offset
        self.y_offset_name = y_offset_name
        self.y_offset_text = y_offset_text
        self.name_color = name_color
        self.text_color = text_color

        self.cnt = 0
        self.current_name = ""
        self.current_text = ""
        self.name_surface = self.font.render("", True, self.name_color)
        self.text_surfaces = []
        self.event_video_manager = None

    def update_text(self):
        if self.cnt < len(dialogue):
            line = dialogue[self.cnt]
            self.current_name = line["name"]
            
            # Event video logic (similar to menu_2.py)
            current_line_data = dialogue[self.cnt - 1] if self.cnt > 0 else None
            if current_line_data and current_line_data['id'] == 4:
                print(f"{self.cnt}")
            else:
                if self.event_video_manager:
                    self.event_video_manager = None
            
            self.current_text = line["text"]
            lines = self.current_text.split('\n') 
            
            self.name_surface = self.font.render(self.current_name, True, self.name_color)
            self.text_surfaces = [self.font.render(text_line, True, self.text_color) for text_line in lines]

            self.cnt += 1
            return True # Indicate that text was updated
        else:
            return False # Indicate no more text

    def draw_text(self):
        # 💬 名前を描画
        name_rect = self.name_surface.get_rect(left=100 + self.x_offset, bottom=SCREEN_HEIGHT - 250)
        self.screen.blit(self.name_surface, name_rect)

        # 💬 セリフを描画 (複数行対応)
        y_position = SCREEN_HEIGHT - 200 # 最初の行の開始Y座標
        line_spacing = self.font.get_linesize()

        for surface in self.text_surfaces:
            text_rect = surface.get_rect(left=300 + self.x_offset, top=y_position)
            self.screen.blit(surface, text_rect)
            y_position += line_spacing

    def get_event_video_manager(self):
        return self.event_video_manager

    def get_cnt(self):
        return self.cnt

    def get_dialogue_length(self):
        return len(dialogue)

    def get_current_dialogue_line(self):
        if self.cnt > 0 and self.cnt <= len(dialogue):
            return dialogue[self.cnt - 1]
        return None

    def update_event_video_frame(self):
        if self.event_video_manager:
            self.event_video_manager.update_video_frame()

    def draw_event_video(self):
        if self.event_video_manager:
            self.event_video_manager.draw_video(self.screen)
