from os import walk
from csv import reader
import pygame


def import_surfaces(path):
    surface_list = []
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            img_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(img_surface)

    return surface_list


def import_csv(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

