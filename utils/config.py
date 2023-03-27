WIDTH = 1280
HEIGHT = 720
TILE_SIZE = 64
FPS = 60

HEALTH_BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG_COLOR = (113, 221, 238)
UI_BORDER = (34, 34, 34)

UI_FONT = 'utils/font/joystix.ttf'
PLAYER_PATH = 'sprites/graphics/player/'

WEAPON_DATA = {
    'sword': {'cooldown': 100, 'damage': 40, 'graphic': 'sprites/graphics/weapons/sword/full.png'}
}

MONSTER_DATA = {
    'squid': {'health': 100, 'damage': 20, 'attack_type': 'slash', 'speed': 3, 'resistance': 3, 'attack_radius': 64,
              'vision_radius': 300},
    'raccoon': {'health': 200, 'damage': 40, 'attack_type': 'claw', 'speed': 3, 'resistance': 3, 'attack_radius': 100,
                'vision_radius': 400}
}
