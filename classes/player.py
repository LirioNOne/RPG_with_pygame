import pygame, sys
from utils import config
from utils.import_folder import import_surfaces
from classes.entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, collided_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('sprites/graphics/player/down/idle_down.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE), )
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -5)
        self.pos = pos
        self.collided_sprites = collided_sprites

        self.attacking = False
        self.attack_cooldown = 100
        self.attack_time = None
        self.status = 'down'
        self.stats = {'health': 150, 'attack': 10, 'speed': 5}
        self.health = self.stats['health']
        self.speed = self.stats['speed']
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.vulnerable = True
        self.hurt_time = None
        self.invincibility_duration = 500

        self.player_assets()

    def player_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_move': [], 'left_move': [], 'up_move': [], 'down_move': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
        for animation in self.animations.keys():
            player_path = config.PLAYER_PATH + animation
            self.animations[animation] = import_surfaces(player_path)

    def event(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.create_attack()
            self.attack_time = pygame.time.get_ticks()

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + config.WEAPON_DATA['sword']['cooldown']:
                self.destroy_attack()
                self.attacking = False

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_status(self):
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if 'move' in self.status:
                self.status = self.status.replace('_move', '')
            if 'attack' not in self.status:
                self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

        if self.direction.x != 0 or self.direction.y != 0:
            if 'move' not in self.status:
                self.status = self.status + '_move'
        else:
            if 'move' in self.status:
                self.status = self.status.replace('_move', '')

    def get_full_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = config.WEAPON_DATA['sword']['damage']

        return base_damage + weapon_damage

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.alpha_change()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.event()
        self.move(self.speed)
        self.cooldown()
        self.get_status()
        self.animate()
