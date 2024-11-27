import random
import math

WIN_WIDTH = 640
WIN_HEIGHT = 480
FPS = 60
TILESIZE = 32

PLAYER_LAYER = 4
BLOCK_LAYER = 2
GROUND_LAYER = 1
ENEMY_LAYER = 3
PROJECTILE_LAYER = 5

PLAYER_SPEED = 5
PLAYER_HP = 3


ENEMY_SPEED = 1
DRUNKARD_SPEED = 2

ENEMY_HP = 3
ENEMY_SIZE = 1.5

DAMAGE_VAL = 1

PROJECTILE_SPEED = 5
PROJECTILE_RADIUS = 5
PROJECTILE_PER_SHOT = 1
PROJECTILE_INTERVAL = 100 #meep
PROJECTILE_COUNT = 5
PROJECTILE_ANGLE = random.uniform(0, 2 * math.pi)


PINK = (255,204,229)
BLACK = (0,0,0)
BLUE = (102,178,255)
GREEN = (204,255,229)
RED = (255,0,0)
PURPLE = (160,32,240)
ORANGE = (255,165,0)
GREY = (128,128,128)

tilemap = [
	'WWWWWWWWWWWWWWWWWWWW',
	'W..................W',
	'W..................W',
	'W..................W',
	'W.........E........W',
	'W..................W',
	'W..................W',
	'W..................W',
	'W.........P........W',
	'W..................W',
	'W..................W',
	'W..................W',
	'W..................W',
	'W..................W',
	'WWWWWWWWWWWWWWWWWWWW',

] #The W represents walls, dots represent nothing there, P is where the player appears


