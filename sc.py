import pygame as pg
import random
pg.init()

def roll_dice():
    return random.randint(1, 6)

def move_player(player, steps):
    player.left += steps * 2


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Snakes and Ladders")

# Create a font object to render the text
font = pg.font.Font(None, 36)
font_surface = font.render("Welcome to the Snakes and Ladders", False, "White")
clock = pg.time.Clock()

# Create a player rect with x, y, width, and height
player_position = [300, 100]


player = pg.Surface((50, 50))
player.fill((250, 0, 0))

# Create a game board surface
board_surface = pg.Surface((300, 300))
board_surface.fill((255, 255, 255))

cell1_surface = pg.Surface((70, 70))
cell1_surface.fill((0, 0, 0))

cell2_surface = pg.Surface((70, 70))
cell2_surface.fill((0, 0, 0))

cell3_surface = pg.Surface((70, 70))
cell3_surface.fill((0, 0, 0))

cell4_surface = pg.Surface((70, 70))
cell4_surface.fill((0, 0, 0))

cell5_surface = pg.Surface((70, 70))
cell5_surface.fill((0, 0, 0))

cell6_surface = pg.Surface((70, 70))
cell6_surface.fill((0, 0, 0))

cells_positions = {
    1: (255, 155),
    2: (330, 155),
    3: (405, 155),
    4: (255, 230),
    5: (330, 230),
    6: (405, 230)

}
def move_player_to_cell(cell):
    player_position[0], player_position[1] = cells_positions[cell]
    return player_position

def handle_key_press(key, player_position):
    if key[pg.K_1]:
        player_position = move_player_to_cell(1)
    elif key[pg.K_2]:
        player_position = move_player_to_cell(2)
    elif key[pg.K_3]:
        player_position = move_player_to_cell(3)
    elif key[pg.K_4]:
        player_position = move_player_to_cell(4)
    elif key[pg.K_5]:
        player_position = move_player_to_cell(5)
    elif key[pg.K_6]:
        player_position = move_player_to_cell(6)
    return player_position


running = True
while running:

    # Fill the screen with black, so that the previous trail of the player rect is removed
    screen.fill((0, 0, 0))
    screen.blit(board_surface, (250, 150))
    screen.blit(cell1_surface, (255, 155))
    screen.blit(cell2_surface, (330, 155))
    screen.blit(cell3_surface, (405, 155))
    screen.blit(cell4_surface, (255, 230))
    screen.blit(cell5_surface, (330, 230))
    screen.blit(cell6_surface, (405, 230))
    screen.blit(player, (player_position[0], player_position[1]))
    
    screen.blit(font_surface, (175, 50))

    # Get the keys that are pressed
    key = pg.key.get_pressed()
    player_position = handle_key_press(key, player_position)

    # Check if the quit event is triggered
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    # Draw the board surface with centre position (250, 150) at top left
    


    pg.display.flip()
    clock.tick(60)
pg.quit()

