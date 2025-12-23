import sys
import os

# Add the 'file' directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'file'))

import pygame
from running_1 import Start_Screen
from menu_2 import MOVieStart
from practice4_ai import MainGameScene # Import MainGameScene

if __name__ == "__main__":
    pygame.init()
    
    # First scene: running_1.py
    start_screen = Start_Screen()
    next_scene = start_screen.display_text() # Get return value

    if next_scene == "menu_2":
        print("Transitioning to menu_2.py")
        movie = MOVieStart()
        answer, next_scene = movie.display_text() # Get return value from menu_2.py

        if next_scene == "practice": # This will now trigger practice4_ai
            print("Transitioning to practice4_ai.py")
            game_scene = MainGameScene(answer=answer) # Instantiate MainGameScene with answer
            game_scene.main() # Call main method
    
    pygame.quit()
    sys.exit()