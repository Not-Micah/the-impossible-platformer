import pygame
from random import randint
from settings import tile_size
from support import import_folder
from settings import screen_width

class CrateParticles:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []

    def clear(self):
        
        self.particles.clear()

    def draw(self, crate):
        # range
        x_lowest = crate.rect.x - 10
        x_highest = crate.rect.x + crate.image.get_width() + 10
        y_lowest = crate.rect.y - 5
        y_highest = crate.rect.y + 5

        # generating value
        particle_x = randint(x_lowest, x_highest)
        particle_y = randint(y_lowest, y_highest)

        # random particle movement
        x_vel = randint(0, 20)/10 - 1
        y_vel = -2

        # particle timer
        particle_time = randint(1, 3)

        self.particles.append([[particle_x, particle_y], [x_vel, y_vel], particle_time])

        for particle in self.particles:

            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[1][1] += 0.6
            particle[2] -= 0.10

            pygame.draw.circle(self.screen, (205, 127, 50), (particle[0]), int(particle[2]))

        if particle[2] <= 0:
            self.particles.remove(particle)

class EnemyKillEfect:
    def __init__(self, screen, enemy):

        self.screen = screen

        # timing text
        self.timer = 0
        self.timer_speed = 1.5
        self.time_limit = 50

        # font
        self.font = pygame.font.Font('./graphics/Minecraft.ttf', 25)

        # position
        self.enemy_x = enemy.rect.x
        self.enemy_y = enemy.rect.y

    def update(self, world_shift):
        self.enemy_x += world_shift

    def draw_text(self):

        self.text_shadow = self.font.render('+ kill', True, (64, 64, 64))
        self.text = self.font.render('+ kill', True, (255, 255, 255))

        self.screen.blit(self.text_shadow, (self.enemy_x + 1, self.enemy_y + 1))
        self.screen.blit(self.text, (self.enemy_x, self.enemy_y))

        self.timer += self.timer_speed

class AudioEffect:
    def __init__(self, path, volume):
        self.sound = pygame.mixer.Sound(path)
        self.sound.set_volume(volume)

    def play_sound(self):
        self.sound.play()

    def stop_sound(self):
        pygame.mixer.stop()

class JumpParticles:
    def __init__(self, x, y):
        # frames
        self.frames = import_folder('./graphics/jump_particles')
        self.frame_speed = 0.25
        self.frame_index = 0
        
        # init image
        self.image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1.5, self.image.get_height() * 1.5))

        # coordinates
        self.x = x
        self.y = y

        # rect
        self.rect = self.frames[self.frame_index].get_rect(center=(self.x, self.y))
        self.end = False

    def animate(self):
        self.frame_index += self.frame_speed

        if self.frame_index >= len(self.frames):
            self.frame_index = 0
            self.end = True

        self.image = self.frames[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1.5, self.image.get_height() * 1.5))

    def update(self, shift):
        self.animate()
        self.rect.x += shift

class DirectionArrow:
    def __init__(self, screen):
        self.screen = screen
        self.frames = import_folder('./graphics/arrow')
        self.frame_speed = 0.05
        self.frame_index = 0

        # image
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(screen_width-125, 125))

    def animate(self):
        self.frame_index += self.frame_speed

        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        
        self.image = self.frames[int(self.frame_index)]

    def draw(self):
        self.animate()
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        