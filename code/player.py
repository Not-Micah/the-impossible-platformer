import pygame 
from support import import_folder
from effects import AudioEffect, JumpParticles

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.display_surface = surface
		
		# particles
		self.jump_particles = []

		# audio effects
		self.jump_sfx = AudioEffect('./sfx/jump_sound.mp3', 0.1)

		# player health/mana
		self.dead = False
		self.mana = 100

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 5
		self.gravity = 0.8
		self.jump_speed = -16

		# player status
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = True
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False
		self.opening = False
		self.invisible = False
		self.attacking = False

		# mask
		self.mask = pygame.mask.from_surface(self.image)

	def import_character_assets(self):
		character_path = './graphics/character/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'shoot':[],'thrust':[], 
		'invisible_idle':[], 'invisible_jump':[], 'invisible_run':[], 'invisible_fall': [], 'invisible_thrust': []}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image

		# resizing character
		self.image = pygame.transform.scale(self.image, ((self.image.get_width() * 3), (self.image.get_height() * 3)))

		# set the rect
		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(topleft = self.rect.topleft)
		elif self.on_ceiling:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)

	def get_input(self):
		keys = pygame.key.get_pressed()
		
		# invisibility
		if keys[pygame.K_LSHIFT] and self.mana > 0:
			self.invisible = True
			self.mana -= 0.5
		else:
			self.invisible = False

		# movements
		if keys[pygame.K_d]:
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_a]:
			self.direction.x = -1
			self.facing_right = False
		else:
			self.direction.x = 0

		# crates
		if keys[pygame.K_s]:
			self.opening = True
		elif keys[pygame.K_f] == False:
			self.opening = False

		# attacks
		if pygame.mouse.get_pressed()[0] == True and self.mana > 0 and self.on_ground: 
			self.attacking = True
			self.player_attack()
		else:
			self.attacking = False

		# jump
		if keys[pygame.K_w] and self.on_ground:
			self.jump_sfx.play_sound()
			self.jump()

	def get_status(self):

		if self.direction.y < 0:
			if self.invisible == True:
				self.status = 'invisible_jump'
			else:
				self.status = 'jump'

		elif self.direction.y > 1:
			if self.invisible == True:
				self.status = 'invisible_fall'
			else:
				self.status = 'fall'

		else:
			if self.direction.x != 0:
				if self.invisible == True:
					self.status = 'invisible_run'
				else:
					self.status = 'run'

			else:
				if self.invisible == True:
					self.status = 'invisible_idle'
				else:
					self.status = 'idle'

		if self.attacking == True:
			if self.invisible == True:
				self.status = 'invisible_thrust'
			else:
				self.status = 'thrust'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed

		# particles
		particles = JumpParticles(self.rect.x, self.rect.y)
		self.jump_particles.append(particles)

	def player_attack(self):
		if self.facing_right == True:
			self.direction.x += 1
		else:
			self.direction.x -= 1
		self.mana -= 0.5

	def update(self):
		self.get_input()
		self.get_status()
		self.animate()
		self.mask = pygame.mask.from_surface(self.image)

		if self.status == 'idle' or self.status == 'invisible_idle': 
			self.animation_speed = 0.05
		else: 
			self.animation_speed = 0.15
