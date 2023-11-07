import random, pygame

run_menu = True
run = True
show_high_score = True

playing_music = True
game_is_over = False
pause = False
move_up = False
move_down = False
move_right = False
move_left = False
width = 1800
height = 800
window = (width, height)
center_screen = (width // 2, height // 2)
midtop_screen = (width // 2, 0)
coordinates_scrore = (width // 2, 30)
pos_x_window = 0
pos_y_window = 0
qty_enemies= 3
FPS = 25
height_rect_submarine = 85
width_rect_submarine = 155
submarine_speed = 10
qty_mines = 10
width_mine = 35
height_mine = 35
screen = pygame.display.set_mode((width, height))

nave_rect_center = (width // 2, height // 2)
height_rect_enemies = 85
width_rect_enemies = 155
pos_x_ship_enemies = width // 2 
pos_y_ship_enemies = height * 0.25
ship_enemy_speed = -5
front_bullet = None
width_front_bullet = 55
height_front_bullet = 35
width_top_bullet = 25
height_top_bullet = 45
width_detroyer_bullet = 25
height_destroyer_bullet = 45

top_bullet = None
width_bullet = 15
height_bullet = 70
max_front_bullets_count = 5
front_bullet_count = 0
max_top_bullets_count = 5
top_bullet_count = 0
speed_bullet = 5
speed_top_bullet = -5
submarine_shield = 100
score = 0
qty_coins = 2
width_rect_coin = 25
height_rect_coin = 25

width_rect_explotion = 50
height_rect_explotion = 50
num_frames_explotion = 8

#balas detroyer

time_last_shot = 0
shot_interval = 3
destroyer_hit = False
new_destroyer_delay = 3000  
time_last_destroyer_hit = 0  

# boton

width_button = 400
height_button = 100


#----Colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)
LIGHTGRAY = (211, 211, 211)
DARKGRAY = (169, 169, 169)
LAVENDER = (230, 230, 250)
INDIGO = (75, 0, 130)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BEIGE = (245, 245, 220)
TURQUOISE = (64, 224, 208)
CORAL = (255, 127, 80)
VIOLET = (238, 130, 238)
KHAKI = (240, 230, 140)
AQUAMARINE = (127, 255, 212)
TOMATO = (255, 99, 71)
CHOCOLATE = (210, 105, 30)
SALMON = (250, 128, 114)
PERU = (205, 133, 63)
CRIMSON = (220, 20, 60)
LIME = (0, 255, 0)
DODGERBLUE = (30, 144, 255)
FIREBRICK = (178, 34, 34)
GOLDENROD = (218, 165, 32)
LAWNGREEN = (124, 252, 0)
MEDIUMAQUAMARINE = (102, 205, 170)
MEDIUMBLUE = (0, 0, 205)
MEDIUMORCHID = (186, 85, 211)
MEDIUMPURPLE = (147, 112, 219)
MEDIUMSEAGREEN = (60, 179, 113)
MEDIUMSLATEBLUE = (123, 104, 238)
MEDIUMSPRINGGREEN = (0, 250, 154)
MEDIUMTURQUOISE = (72, 209, 204)
MEDIUMVIOLETRED = (199, 21, 133)

color_hover = INDIGO