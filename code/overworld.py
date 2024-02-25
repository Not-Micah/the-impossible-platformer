import pygame
from effects import AudioEffect, DirectionArrow
from game_data import level_data
from support import import_folder

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed, count, position):
        super().__init__()
        # initializing
        self.pos = position
        self.frames = import_folder(f'./graphics/level_node/{self.pos}')
        self.available = False

        # settings
        self.frame_speed = 0.05
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 4, self.image.get_height() * 4))

        if status == 'available':
            self.available = True
        else:
            self.available = False
        
        # position + collision
        self.rect = self.image.get_rect(center=pos)
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2), self.rect.centery - (icon_speed/2), icon_speed, icon_speed)

    def update(self):
        if self.available:
            self.frame_index += self.frame_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 4, self.image.get_height() * 4))

        else:
            new_surf = self.image.copy()
            new_surf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(new_surf, (0, 0))

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.facing_left = False

        # image attributes
        self.original_image = pygame.transform.scale(pygame.image.load('./graphics/menus/icon.png'), (80, 78))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)


    def reverse(self, status):
        if status == 'next':
            self.facing_left = False
            self.image = self.original_image

        if status == 'previous' and not self.facing_left:
            self.facing_left = True
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.rect.center = self.pos
    
class Overworld:
    def __init__(self, start_level, max_level, current_level, surface):
        # switch to level
        self.activate_level = False

        # setup
        self.display_surface = surface
        self.current_level = current_level
        self.max_level = max_level

        # polish
        self.arrow = DirectionArrow(self.display_surface)

        # movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0 ,0)
        self.speed = 8

        # sprites
        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        count = 0 

        self.nodes = pygame.sprite.Group()
        
        for index, node_data in enumerate(level_data.values()):
            
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed, count, index+1)

            else:
                node_sprite = Node(node_data['node_pos'], 'lock', self.speed, count, index+1)

            self.nodes.add(node_sprite)

        count += 1

    def draw_paths(self):
        if self.max_level > 0:
            # list comprehension to get line coords for levels under max level
            points = [node['node_pos'] for index, node in enumerate(level_data.values()) if index <= self.max_level]

            # drawing all the lines from the points
            pygame.draw.lines(self.display_surface, (34, 33, 42), False, points, 6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        
        # checking for input
        keys = pygame.key.get_pressed()

        # getting mouse pos
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rect = pygame.rect.Rect(mouse_x, mouse_y, 25, 25)
        mouse_rect.center = (mouse_x, mouse_y)

        if not self.moving:

            if keys[pygame.K_d] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True

            elif keys[pygame.K_a] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True

            # selecting level
            if mouse_rect.colliderect(self.nodes.sprites()[self.current_level].rect) and pygame.mouse.get_pressed()[0]:
                self.activate_level = True

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)

        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)

        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
        
        self.icon.sprite.reverse(target)
        return (end - start).normalize() # normalizing changes a point into a direction

    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]

            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def run(self):
        self.nodes.update()
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)

        with open('./memory/arrow.txt', 'r') as f:
            if int(f.readline()) == 0:
                self.arrow.draw()
    
        