import pygame
from utils import import_folder


class ParticlesData:
    def __init__(self):
        self.frames = {
            'squid': import_folder.import_surfaces('sprites/graphics/particles/smoke_orange'),
            'raccoon': import_folder.import_surfaces('sprites/graphics/particles/raccoon'),

            'slash': import_folder.import_surfaces('sprites/graphics/particles/slash'),
            'claw': import_folder.import_surfaces('sprites/graphics/particles/claw')
        }

    def create_particles(self, attack_type, pos, groups):
        animation_frames = self.frames[attack_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.2
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
