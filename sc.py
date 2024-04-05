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

cell7_surface = pg.Surface((70, 70))
cell7_surface.fill((0, 0, 0))

cell8_surface = pg.Surface((70, 70))
cell8_surface.fill((0, 0, 0))

cell9_surface = pg.Surface((70, 70))
cell9_surface.fill((0, 0, 0))

cells_positions = {
    cell1_surface: (255, 155),
    cell2_surface: (330, 155),
    cell3_surface: (405, 155),
    cell4_surface: (255, 230),
    cell5_surface: (330, 230),
    cell6_surface: (405, 230),
    cell7_surface: (255, 305),
    cell8_surface: (330, 305),
    cell9_surface: (405, 305)

}
def move_player_to_cell(cell):
    player_position[0], player_position[1] = cells_positions[cell]
    return player_position

def draw_snake(starting_cell, ending_cell):
    # Create a rectangle object for cell1_surface
    starting_rect = starting_cell.get_rect()
    ending_rect = ending_cell.get_rect()

    # Set the top-left position of cell1_surface on the screen
    starting_rect.topleft = cells_positions[starting_cell]
    ending_rect.topleft = cells_positions[ending_cell]

    # Draw a line from the center of cell1_rect to the point (370, 300) with a thickness of 5
    pg.draw.line(screen, (255, 0, 0), starting_rect.center, ending_rect.center, 5)

def draw_ladder(starting_cell, ending_cell):
    # Create a rectangle object for cell1_surface
    starting_rect = starting_cell.get_rect()
    ending_rect = ending_cell.get_rect()

    # Set the top-left position of cell1_surface on the screen
    starting_rect.topleft = cells_positions[starting_cell]
    ending_rect.topleft = cells_positions[ending_cell]

    # Draw a line from the center of cell1_rect to the point (370, 300) with a thickness of 5
    pg.draw.line(screen, (0, 255, 0), starting_rect.center, ending_rect.center, 5)


def handle_key_press(key, player_position):
    if key[pg.K_1]:
        player_position = move_player_to_cell(cell1_surface)
    elif key[pg.K_2]:
        player_position = move_player_to_cell(cell2_surface)
    elif key[pg.K_3]:
        player_position = move_player_to_cell(cell3_surface)
    elif key[pg.K_4]:
        player_position = move_player_to_cell(cell4_surface)
    elif key[pg.K_5]:
        player_position = move_player_to_cell(cell5_surface)
    elif key[pg.K_6]:
        player_position = move_player_to_cell(cell6_surface)
    elif key[pg.K_7]:
        player_position = move_player_to_cell(cell7_surface)
    elif key[pg.K_8]:
        player_position = move_player_to_cell(cell8_surface)
    elif key[pg.K_9]:
        player_position = move_player_to_cell(cell9_surface)
    return player_position

running = True
while running:

    # Fill the screen with black, so that the previous trail of the player rect is removed
    screen.fill((0, 0, 0))
    screen.blit(board_surface, (250, 150))

    screen.blit(cell1_surface, cells_positions[cell1_surface])
    screen.blit(cell2_surface, cells_positions[cell2_surface])
    screen.blit(cell3_surface, cells_positions[cell3_surface])
    screen.blit(cell4_surface, cells_positions[cell4_surface])
    screen.blit(cell5_surface, cells_positions[cell5_surface])
    screen.blit(cell6_surface, cells_positions[cell6_surface])
    screen.blit(cell7_surface, cells_positions[cell7_surface])
    screen.blit(cell8_surface, cells_positions[cell8_surface])
    screen.blit(cell9_surface, cells_positions[cell9_surface])

    screen.blit(player, (player_position[0], player_position[1]))
    
    screen.blit(font_surface, (175, 50))

    draw_snake(cell1_surface, cell4_surface)
    draw_ladder(cell2_surface, cell6_surface)

    # Get the keys that are pressed
    key = pg.key.get_pressed()
    player_position = handle_key_press(key, player_position)

    # Check if the quit event is triggered
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    


    pg.display.flip()
    clock.tick(60)
pg.quit()

