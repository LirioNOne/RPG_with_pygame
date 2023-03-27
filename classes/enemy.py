import pygame
from classes.entity import Entity
from utils.import_folder import import_surfaces
from utils import config


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, collided_sprites, attacking_player):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.status = 'idle'
        self.import_monster(monster_name)

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -5)
        self.collided_sprites = collided_sprites

        self.monster_name = monster_name
        monster_stats = config.MONSTER_DATA[self.monster_name]
        self.health = monster_stats['health']
        self.speed = monster_stats['speed']
        self.damage = monster_stats['damage']
        self.resistance = monster_stats['resistance']
        self.attack_type = monster_stats['attack_type']
        self.vision_radius = monster_stats['vision_radius']
        self.attack_radius = monster_stats['attack_radius']
        self.can_attack = True
        self.attack_cooldown = 1000
        self.attack_time = None
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
        self.attacking_player = attacking_player

    def import_monster(self, monster_name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'sprites/graphics/monsters/{monster_name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_surfaces(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.vision_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def action(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.attacking_player(self.damage, self.attack_type)
            # print('attack')
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            self.health -= player.get_full_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.alpha_change()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.action(player)
