import pygame

from classes.ysortcameragruop import YSortCameraGroup
from utils import config, import_folder
from classes.tile import Tile
from classes.player import Player
from classes.enemy import Enemy
from classes.ui import UI
from classes.weapon import Weapon
from particles import ParticlesData


class Level:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.collided_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.game_over = False
        self.font = pygame.font.Font(config.UI_FONT, 48)
        self.game_over_text = self.font.render('Game Over', True, config.RED)
        self.text_rect = self.game_over_text.get_rect()
        self.text_rect.center = (config.WIDTH // 2, config.HEIGHT // 2)

        self.current_attack = None
        self.ui = UI()
        self.particle_animation = ParticlesData()
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_folder.import_csv('sprites/map/map_FloorBlocks.csv'),
            'entities': import_folder.import_csv('sprites/map/map_Entities.csv')
        }
        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, column in enumerate(row):
                    if column != '-1':
                        pos_x = j * config.TILE_SIZE
                        pos_y = i * config.TILE_SIZE

                        if style == 'boundary':
                            Tile((pos_x, pos_y), [self.collided_sprites], 'invisible')
                        if style == 'entities':
                            if column == '394':
                                self.player = Player((pos_x, pos_y), [self.visible_sprites],
                                                     self.collided_sprites, self.create_attack, self.destroy_attack)
                            else:
                                if column == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(monster_name, (pos_x, pos_y), [self.visible_sprites, self.attackable_sprites],
                                      self.collided_sprites, self.attacking_player)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprite = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprite:
                    for target_sprite in collision_sprite:
                        target_sprite.get_damage(self.player)

    def attacking_player(self, amount, attack_type):
        if self.player.vulnerable:
            if self.player.health <= 0:
                self.game_over = True
                self.game_end()
            else:
                self.player.health -= amount
                if self.player.health <= 0:
                    self.game_over = True
                    self.game_end()
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.particle_animation.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def update(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        self.game_end()

    def game_end(self):
        if self.game_over:
            self.player.kill()
            self.screen.fill(config.BLACK)
            self.screen.blit(self.game_over_text, self.text_rect)