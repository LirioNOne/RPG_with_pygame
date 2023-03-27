import pygame


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.stable_camera_horizontal = self.screen.get_size()[0] // 2
        self.stable_camera_vertical = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.bg_surface = pygame.image.load('sprites/graphics/tilemap/ground.png').convert()
        self.bg_rect = self.bg_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.stable_camera_horizontal
        self.offset.y = player.rect.centery - self.stable_camera_vertical

        floor_offset_pos = self.bg_rect.topleft - self.offset
        self.screen.blit(self.bg_surface, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = []
        for sprite in self.sprites():
            if hasattr(sprite, 'sprite_type'):
                if sprite.sprite_type == 'enemy':
                    enemy_sprites.append(sprite)
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
