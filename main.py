import pygame
import sys
import random

# setting the directory
sys.path.insert(1, 'D:\Pygame Platformer\code')
# imports
from settings import *
from level import Level
from game_data import levels
from overworld import Overworld
from menus import ResetLevelMenu, ExitGameMenu, TutorialMenu

def intro(screen):
    timer = 0

    while timer <= 500:
        logo_screen = pygame.image.load('./graphics/menus/intro.png')
        screen.blit(logo_screen, (0, 0))
        pygame.display.update()
        timer += 1

class Game:
    def __init__(self):
        self.activity_status = 'overworld'
        self.current_level = 0

        # finding current level
        with open('./memory/score.txt', 'r') as f:
            self.max_level = int(f.readline())

        # menu
        self.reset_level_menu = ResetLevelMenu(screen)
        self.exit_game_menu = ExitGameMenu(screen)
        self.tutorial_menu = TutorialMenu(screen)

        self.overworld = Overworld(0, self.max_level, self.current_level, screen)
        self.level = Level(levels[self.current_level], screen)

    def restart_level_progress(self):
        self.level = Level(levels[self.overworld.current_level], screen)

    def update_over_world(self):
        self.overworld = Overworld(0, self.max_level, self.current_level, screen)

    def get_screen_status(self):
        if self.activity_status == 'level' and self.level.activate_overworld:
            self.activity_status = 'overworld'

            if self.level.beat_level_status:

                if self.overworld.current_level == self.max_level:
                    self.current_level = self.overworld.current_level

                    if self.current_level != 5:
                        self.max_level += 1
                        
                    self.update_over_world()

                self.restart_level_progress()

        if self.activity_status == 'overworld' and self.overworld.activate_level:
            self.activity_status = 'level'
            self.overworld.activate_level = False
            self.level = Level(levels[self.current_level], screen)

    def run(self):
        # updating current level
        self.current_level = self.overworld.current_level
        self.get_screen_status()

        # running scenerios
        if self.activity_status == 'overworld':

            if self.reset_level_menu.menu_status:
                self.reset_level_menu.run()

            elif self.exit_game_menu.menu_status:
                self.exit_game_menu.run()

            elif self.tutorial_menu.menu_status:
                self.tutorial_menu.run()

            else:
                self.overworld.run()
                self.reset_level_menu.run()
                self.exit_game_menu.run()
                self.tutorial_menu.run()

            # resetting level option
            if self.reset_level_menu.reset:
                self.max_level = 0
                self.current_level = 0
                self.update_over_world()
                self.reset_level_menu.reset = False

        if self.activity_status == 'level':

            if not self.level.restart_level:
                self.level.run()

            else:
                self.restart_level_progress()
                self.level.run()

# initizializing pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

# window
pygame.display.set_caption('The Impossible Platformer')
pygame.display.set_icon(pygame.image.load('./graphics/menus/icon.png'))
over_world_bg = pygame.image.load('./graphics/overworld_bg.png')

# game function
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or game.exit_game_menu.exit:
                # creating new data in the text file
                with open('./memory/score.txt', 'r+') as f:
                    f.truncate(0)
                    f.write(f'{game.overworld.max_level}')

                pygame.quit()
                sys.exit()

        screen.blit(over_world_bg, (0,0))
        game.run()

        # music
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(
                random.choice(['./sfx/music_1.mp3', './sfx/music_2.mp3', './sfx/music_3.mp3', './sfx/music_4.mp3'])
            )
            pygame.mixer.music.set_volume(0.05)
            pygame.mixer.music.play(-1)

        pygame.display.update()
        clock.tick(60)

# main loop
if __name__ == '__main__':
    intro(screen)
    main()
