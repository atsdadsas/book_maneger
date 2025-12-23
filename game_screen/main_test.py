import pygame
import sys
from confing import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from confing_write_text import TextDisplayManager

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Text Display Test")

# Create a TextDisplayManager instance
text_manager = TextDisplayManager(screen)

# Initial text update
text_manager.update_text()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if text_manager.update_text():
                pass # Text updated, continue
            else:
                running = False # No more text, exit loop

    # Update event video frame if any
    text_manager.update_event_video_frame()

    # Fill the screen
    screen.fill(BLACK)

    # Draw event video if any
    text_manager.draw_event_video()

    # Draw text
    text_manager.draw_text()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()
sys.exit()
