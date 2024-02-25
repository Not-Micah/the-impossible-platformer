import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, f'./graphics/enemy/run/{path}')

        # init image
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 3, self.image.get_height() * 3))
        
        # rect + speed
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3, 5)

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.x += self.speed

    def animate(self):
        self.frame_index += self.frame_speed

        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        
        self.image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (self.image.get_width()  * 3, self.image.get_height() * 3))

    def reverse_image(self):
        if self.speed > 0:
            # true = x axis, false = y axis
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
        self.mask = pygame.mask.from_surface(self.image)
