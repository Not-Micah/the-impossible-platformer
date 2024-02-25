import pygame
import random
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Palm, Timer
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from effects import CrateParticles, EnemyKillEfect, AudioEffect
from menus import ExitLevelMenu

class Level:
    def __init__(self, level_data, surface):
        # sound effect
        self.player_death_sfx = AudioEffect('./sfx/player_death_sound.mp3', 0.3)
        self.enemy_death_sfx = AudioEffect('./sfx/enemy_death_sound.mp3', 0.1)
        self.level_up_sfx = AudioEffect('./sfx/level_up.mp3', 0.5)

        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = 0

        # exit menu
        self.exit_menu = ExitLevelMenu(self.display_surface)
        self.menu_status = False

        # events
        self.activate_overworld = False
        self.restart_level = False
        self.beat_level_status = False

        # particles
        self.display_text = []
        self.crate_particles = CrateParticles(self.display_surface)

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # terain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # timer
        timer_layout = import_csv_layout(level_data['crates'])
        self.timer_sprites = self.create_tile_group(timer_layout, 'timers')

        # foreground palms
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

        # backround palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)
        self.clouds = Clouds(400, level_width, 20)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        crate_count = 0
        timer_count = 0

        # looping over the data to find the index of each tile
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('./graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('./graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'crates':
                        sprite = Crate(tile_size, x, y, crate_count)
                        crate_count += 1

                    if type == 'timers':
                        sprite = Timer(tile_size, x, y, './graphics/timer', timer_count)
                        timer_count += 1

                    if type == 'fg palms':
                        if val == '0': 
                            sprite = Palm(tile_size, x, y, './graphics/terrain/palm_small', 10)
                        if val == '1': 
                            sprite = Palm(tile_size, x, y, './graphics/terrain/palm_large', 60)

                    if type == 'bg palms':
                        sprite = Palm(tile_size, x, y, './graphics/terrain/palm_bg', 60)

                    if type == 'enemies':
                        if val == '0': 
                            sprite = Enemy(tile_size, x, y, 'bat')
                        if val == '1': 
                            sprite = Enemy(tile_size, x, y, 'frog')
                        if val == '2': 
                            sprite = Enemy(tile_size, x, y, 'ghost')

                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
         for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):

                x = col_index * tile_size
                y = row_index * tile_size

                if val == '0':
                    sprite = Player((x, y), self.display_surface)
                    self.player.add(sprite)
                
                if val == '1':
                    target_surface = pygame.image.load('./graphics/character/target.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, target_surface)
                    sprite.image = pygame.transform.scale(sprite.image, (sprite.image.get_width() * 2, sprite.image.get_height() * 2))
                    sprite.rect.x += 25
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            # checking if any of the sprites are colliding with the constraints
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def horizontal_movement_collision(self):
	    player = self.player.sprite
	    player.rect.x += player.direction.x * player.speed

	    collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()

	    for sprite in collidable_sprites:

		    if sprite.rect.colliderect(player.rect):

			    if player.direction.x < 0: 
				    player.rect.left = sprite.rect.right
				    player.on_left = True
				    self.current_x = player.rect.left

			    elif player.direction.x > 0:
				    player.rect.right = sprite.rect.left
				    player.on_right = True
				    self.current_x = player.rect.right

	    if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
		    player.on_left = False
            
	    if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
		    player.on_right = False  

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()

        for sprite in collidable_sprites:

            if sprite.rect.colliderect(player.rect):

                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
            
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def player_enemy_collision(self):
        player = self.player.sprite
        enemies = self.enemy_sprites.sprites()

        # checking for collisions
        for sprite in enemies:
            
            if pygame.sprite.collide_mask(sprite, player) and not player.invisible:
            # if sprite.rect.colliderect(player.rect) and not player.invisible:

                # if player kills enemy
                if player.status == 'thrust' or player.status == 'invisible_thrust':
                    if (player.facing_right and sprite.rect.x > player.rect.x) or (not player.facing_right and player.rect.x > sprite.rect.x):

                        self.enemy_death_sfx.play_sound()
                        sprite.kill()
                        self.display_text.append(EnemyKillEfect(self.display_surface, sprite))

                    else:
                        self.player_death_sfx.play_sound()
                        self.restart_level = True

                # if enemy kills player
                else:
                    if not player.invisible:
                        self.player_death_sfx.play_sound()
                        self.restart_level = True

        # drawing kill text
        for text in self.display_text:

            if text.timer <= text.time_limit:
                text.update(self.world_shift)
                text.draw_text()
                
            else:
                self.display_text.remove(text)

    def open_crates(self):
        player = self.player.sprite
        crates = self.crate_sprites.sprites()
        timers = self.timer_sprites.sprites()

        for crate in crates:

            if ((player.rect.x - crate.rect.x <= 35 and player.rect.x - crate.rect.x >= 0) or (
                crate.rect.x - player.rect.x <= 35 and crate.rect.x - player.rect.x >= 0)) and player.opening:
                
                crate_pos = crate.count
                x_distance = crate.rect.x - player.rect.x

                if x_distance >= -40 and x_distance <= 20:
                    for timer in timers:
                        if timer.count == crate_pos:

                            if timer.completed == True:
                                
                                timer.kill()
                                crate.kill()

                                if player.mana >= 75:
                                    player.mana = 100
                                else:
                                    player.mana += 25

                            else:
                                timer.draw(self.display_surface)
                                self.crate_particles.draw(crate)


        if player.opening == False:
            self.crate_particles.clear()

    def draw_jump_particles(self):
        for particle in self.player.sprite.jump_particles:
            particle.update(self.world_shift)

            if particle.end == True: 
                self.player.sprite.jump_particles.remove(particle)
                break
            else: 
                self.display_surface.blit(particle.image, (particle.rect.x, particle.rect.y))

    def mana_bar(self):
        # getting player mana
        mana = self.player.sprite.mana
        
        # loading bar outline
        bar_outline = pygame.image.load('./graphics/character/mana_bar.png').convert_alpha()
        bar_outline_x = 25
        bar_outline_y = 25

        # drawing mana bar
        self.display_surface.blit(bar_outline, (bar_outline_x, bar_outline_y))

        for x in range(int(mana)):
            pygame.draw.rect(self.display_surface, (152,251,152), pygame.Rect(
            (bar_outline_x + x * 3 + 1), (bar_outline_y + 1), 3, 18))

    def escape_level(self):
        # getting keys
        keys = pygame.key.get_pressed()

        # checking if player clicks on exit
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rect = pygame.rect.Rect(mouse_x, mouse_y, 25, 25)
        mouse_rect.center = (mouse_x, mouse_y)

        if mouse_rect.colliderect(self.exit_menu.screen_exit_icon_rect) and pygame.mouse.get_pressed()[0]: 
            self.menu_status = True

        if self.menu_status == True:
            self.exit_menu.draw()
            self.exit_menu.add_text()

            if mouse_rect.colliderect(self.exit_menu.exit_icon_rect) and pygame.mouse.get_pressed()[0]:
                # stop audio
                self.player_death_sfx.stop_sound()
                self.enemy_death_sfx.stop_sound()

                # exit level
                self.restart_level = True
                self.activate_overworld = True

            if mouse_rect.colliderect(self.exit_menu.return_icon_rect) and pygame.mouse.get_pressed()[0]:
                self.menu_status = False

            if keys[pygame.K_ESCAPE]:
                self.menu_status = False

    def beat_level(self):
        player = self.player.sprite
        
        if self.goal.sprite.rect.colliderect(player.rect):
            self.level_up_sfx.play_sound()
            self.activate_overworld = True
            self.beat_level_status = True

    def run(self):
        # decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # bg palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # timer
        self.timer_sprites.update(self.world_shift, self.player.sprite.opening)
        self.open_crates()

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # player sprites
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.update()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.draw_jump_particles()

        # fg palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)
         
        # water
        self.water.draw(self.display_surface, self.world_shift)

        # events
        self.player_enemy_collision()
        self.mana_bar()
        self.beat_level()

        # escape assets
        self.exit_menu.add_exit_icon()
        self.escape_level()

        # check if player fell
        if self.player.sprite.rect.y >= screen_height:
            self.player_death_sfx.play_sound()
            self.restart_level = True


