import pygame
from settings import screen_height, screen_width

class TextPrompt:
    def __init__(self, text, coordinates, screen):
        # font
        self.font = pygame.font.Font('./graphics/Minecraft.ttf', 20)
        self.text = text

        # screen
        self.screen = screen

        # creating text
        self.text_shadow = self.font.render(str(self.text), True, (64, 64, 64))
        self.text = self.font.render(str(self.text), True, (255, 255, 255))

        # rects
        self.text_rect = self.text.get_rect(center=(coordinates[0], coordinates[1]))

    def draw(self):

        self.screen.blit(self.text_shadow, (self.text_rect.x, self.text_rect.y + 2))
        self.screen.blit(self.text, (self.text_rect.x, self.text_rect.y))

class ExitLevelMenu:
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        # screen exit icon
        self.screen_exit_icon = pygame.image.load('./graphics/menus/screen_icon.png')
        self.screen_exit_icon_rect = self.screen_exit_icon.get_rect(center=(screen_width-50, 50))
    
        # menu base
        self.menu_base = pygame.image.load('./graphics/menus/exit_menu.png')
        self.menu_base_rect = self.menu_base.get_rect(center=(screen_width//2, screen_height//2))

        # exit icon
        self.exit_icon = pygame.image.load('./graphics/menus/exit_icon.png')
        self.exit_icon_rect = self.exit_icon.get_rect(center=(screen_width//2 - 150, screen_height//2))

        # return icon
        self.return_icon = pygame.image.load('./graphics/menus/return_icon.png')
        self.return_icon_rect = self.return_icon.get_rect(center=(screen_width//2 + 150, screen_height//2))

        # text
        self.text = TextPrompt('Are You Sure You Want To Exit The Level?', (screen_width//2, screen_height//2 - 75), self.screen)

    def add_exit_icon(self):
        self.screen.blit(self.screen_exit_icon, (self.screen_exit_icon_rect.x, self.screen_exit_icon_rect.y))

    def add_text(self):
        self.text.draw()

    def draw(self):
        # drawing menu
        self.screen.blit(self.menu_base, (self.menu_base_rect.x, self.menu_base_rect.y))
        self.screen.blit(self.exit_icon, (self.exit_icon_rect.x, self.exit_icon_rect.y))
        self.screen.blit(self.return_icon, (self.return_icon_rect.x, self.return_icon_rect.y))
        
class ResetLevelMenu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_status = False
        self.reset = False
        self.menu = ExitLevelMenu(self.screen)

        # screen exit icon
        self.menu.screen_exit_icon = pygame.image.load('./graphics/menus/reset_icon.png')
        self.menu.screen_exit_icon_rect = self.menu.screen_exit_icon.get_rect(center=(screen_width-200, 50))
    
        # menu base
        self.menu.menu_base = pygame.image.load('./graphics/menus/exit_menu.png')
        self.menu.menu_base_rect = self.menu.menu_base.get_rect(center=(screen_width//2, screen_height//2))

        # text prompt
        self.text = TextPrompt('Are You Sure You Want To Reset Your Progress?', (screen_width//2, screen_height//2 - 75), self.screen)

    def reset_progress(self):
        # getting keys
        keys = pygame.key.get_pressed()
        
        # checking if player clicks on exit
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rect = pygame.rect.Rect(mouse_x, mouse_y, 25, 25)
        mouse_rect.center = (mouse_x, mouse_y)

        if mouse_rect.colliderect(self.menu.screen_exit_icon_rect) and pygame.mouse.get_pressed()[0]:
            self.menu_status = True

        if self.menu_status == True:
            self.menu.draw()
            self.text.draw()

            if keys[pygame.K_ESCAPE]:
                self.menu_status = False

            if self.menu.exit_icon_rect.colliderect(mouse_rect) and pygame.mouse.get_pressed()[0]:
                self.reset = True
                self.menu_status = False

                # reset text file
                with open('./memory/score.txt', 'r+') as f:
                    f.truncate(0)
                    f.write('0')

                # reset arrow file
                with open('./memory/arrow.txt', 'r+') as f:
                    f.truncate(0)
                    f.write('0')

            if self.menu.return_icon_rect.colliderect(mouse_rect) and pygame.mouse.get_pressed()[0]:
                self.menu_status = False

    def run(self):
        self.menu.add_exit_icon()
        self.reset_progress()

class ExitGameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_status = False
        self.exit = False
        self.menu = ExitLevelMenu(self.screen)

        # screen exit icon
        self.menu.screen_exit_icon = pygame.image.load('./graphics/menus/screen_icon.png')
        self.menu.screen_exit_icon_rect = self.menu.screen_exit_icon.get_rect(center=(screen_width-50, 50))
    
        # menu base
        self.menu.menu_base = pygame.image.load('./graphics/menus/exit_menu.png')
        self.menu.menu_base_rect = self.menu.menu_base.get_rect(center=(screen_width//2, screen_height//2))

        # text
        self.text = TextPrompt('Are You Sure You Want To Exit The Game?', (screen_width//2, screen_height//2 - 75), self.screen)


    def menu_load(self):
        # getting keys
        keys = pygame.key.get_pressed()
        
        # checking if player clicks on exit
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rect = pygame.rect.Rect(mouse_x, mouse_y, 25, 25)
        mouse_rect.center = (mouse_x, mouse_y)

        if mouse_rect.colliderect(self.menu.screen_exit_icon_rect) and pygame.mouse.get_pressed()[0]:
            self.menu_status = True

        if self.menu_status == True:
            self.menu.draw()
            self.text.draw()

            if keys[pygame.K_ESCAPE]:
                self.menu_status = False

            if self.menu.exit_icon_rect.colliderect(mouse_rect) and pygame.mouse.get_pressed()[0]:
                self.exit = True

            if self.menu.return_icon_rect.colliderect(mouse_rect) and pygame.mouse.get_pressed()[0]:
                self.menu_status = False

    def run(self):
        self.menu.add_exit_icon()
        self.menu_load()

class TutorialMenu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_status = False
    
        # screen icon
        self.screen_icon = pygame.image.load('./graphics/menus/question_icon.png')
        self.screen_icon_rect = self.screen_icon.get_rect(center=(screen_width-125, 50))

        # tutorial image
        self.tutorial_image = pygame.image.load('./graphics/menus/tutorial_menu.png')
        self.tutorial_image_rect = self.tutorial_image.get_rect(center=(screen_width//2, screen_height//2))

        # exit tutorial
        self.exit_icon = pygame.image.load('./graphics/menus/screen_icon.png')
        self.exit_icon_rect = self.exit_icon.get_rect(center=(screen_width-300, 250))

    def draw_icon(self):
        self.screen.blit(self.screen_icon, (self.screen_icon_rect.x, self.screen_icon_rect.y))

    def display(self):
        # getting keys
        keys = pygame.key.get_pressed()
        
        # checking if player clicks on exit
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rect = pygame.rect.Rect(mouse_x, mouse_y, 25, 25)
        mouse_rect.center = (mouse_x, mouse_y)

        if mouse_rect.colliderect(self.screen_icon_rect) and pygame.mouse.get_pressed()[0]:
            self.menu_status = True

        if self.menu_status == True:
            self.screen.blit(self.tutorial_image, (self.tutorial_image_rect.x, self.tutorial_image_rect.y))
            self.screen.blit(self.exit_icon, (self.exit_icon_rect.x, self.exit_icon_rect.y))

            with open('./memory/arrow.txt', 'r+') as f:
                f.truncate(0)
                f.write(str(1))

            if keys[pygame.K_ESCAPE]:
                self.menu_status = False

            if mouse_rect.colliderect(self.exit_icon_rect) and pygame.mouse.get_pressed()[0]:
                self.menu_status = False

    def run(self):
        self.draw_icon()
        self.display()