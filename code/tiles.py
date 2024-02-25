import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift

class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class Crate(StaticTile):
    def __init__(self, size, x, y, count):
        super().__init__(size, x, y, pygame.image.load('./graphics/terrain/crate.png').convert_alpha())
        offset_y = y + size
        self.count = count
        self.rect = self.image.get_rect(bottomleft = (x, offset_y))

class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_speed = 0.15
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += self.frame_speed

        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift

class Palm(AnimatedTile):
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)
        self.frame_speed = 0.075

    def animate(self):
        self.frame_index += self.frame_speed

        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        
        self.image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 3.25, self.image.get_height() * 3.25))

class Timer(AnimatedTile):
    def __init__(self, size, x, y, path, count):
        super().__init__(size, x, y, path)

        # offsets
        offset_y = y + size + 2
        offset_x = x - 1

        # animation variables
        self.count = count
        self.frame_speed = 0.05
        self.completed = False
        self.rect = self.image.get_rect(bottomleft = (offset_x, offset_y))

    def update(self, shift, shifting):
        self.rect.x += shift

        if shifting == False:
            self.frame_index = 0

    def draw(self, screen):
        if self.frame_index + self.frame_speed <= len(self.frames):
            self.frame_index += self.frame_speed
            
        else:
            self.completed = True

        self.image = self.frames[int(self.frame_index)]
        screen.blit(self.image, (self.rect.x, self.rect.y))