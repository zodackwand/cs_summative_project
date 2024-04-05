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


class Cell():
    def __init__(self, surface=[70, 70], rect=None, position=[0, 0]):
        self.surface = pg.Surface(surface)
        self.rect = self.surface.get_rect()
        self.rect.topleft = position
        self.position = position

    def set_color(self, array):
        self.surface.fill(array)

    def set_position(self, array):
        self.position = array
        self.rect.topleft = array

player = Cell(position=[300, 100])
player.set_color([200, 50, 50])

# Create a game board surface
board_surface = pg.Surface((300, 300))
board_surface.fill((255, 255, 255))

cell1 = Cell(position=[255, 155])
cell1.set_color([0, 0, 0])

cell2 = Cell(position=[330, 155])
cell2.set_color([0, 0, 0])

cell3 = Cell(position=[405, 155])
cell3.set_color([0, 0, 0])

cell4 = Cell(position=[255, 230])
cell4.set_color([0, 0, 0])

cell5 = Cell(position=[330, 230])
cell5.set_color([0, 0, 0])

cell6 = Cell(position=[405, 230])
cell6.set_color([0, 0, 0])

cell7 = Cell(position=[255, 305])
cell7.set_color([0, 0, 0])

cell8 = Cell(position=[330, 305])
cell8.set_color([0, 0, 0])

cell9 = Cell(position=[405, 305])
cell9.set_color([0, 0, 0])

def change_position_to_cell(cell):
    player.rect.topleft = cell.rect.topleft
    player.position = cell.position
    return player.rect.topleft

def draw_snake(start, end):
    # Draw a line from the center of thickness of 5
    pg.draw.line(screen, (255, 0, 0), start.rect.center, end.rect.center, 5)

def draw_ladder(start, end):
    # Draw a line from the center of thickness of 5
    pg.draw.line(screen, (0, 255, 0), start.rect.center, end.rect.center, 5)

def update_cells():
    screen.blit(cell1.surface, cell1.rect)
    screen.blit(cell2.surface, cell2.rect)
    screen.blit(cell3.surface, cell3.rect)
    screen.blit(cell4.surface, cell4.rect)
    screen.blit(cell5.surface, cell5.rect)
    screen.blit(cell6.surface, cell6.rect)
    screen.blit(cell7.surface, cell7.rect)
    screen.blit(cell8.surface, cell8.rect)
    screen.blit(cell9.surface, cell9.rect)


def handle_key_press(key):
    if key[pg.K_1]:
        player.position = change_position_to_cell(cell1)
    elif key[pg.K_2]:
        player.position = change_position_to_cell(cell2)
    elif key[pg.K_3]:
        player.position = change_position_to_cell(cell3)
    elif key[pg.K_4]:
        player.position = change_position_to_cell(cell4)
    elif key[pg.K_5]:
        player.position = change_position_to_cell(cell5)
    elif key[pg.K_6]:
        player.position = change_position_to_cell(cell6)
    elif key[pg.K_7]:
        player.position = change_position_to_cell(cell7)
    elif key[pg.K_8]:
        player.position = change_position_to_cell(cell8)
    elif key[pg.K_9]:
        player.position = change_position_to_cell(cell9)
    return player.position

running = True
while running:

    # Fill the screen with black, so that the previous trail of the player rect is removed
    screen.fill((0, 0, 0))
    screen.blit(board_surface, (250, 150))

    update_cells()

    screen.blit(player.surface, player.rect)
    
    screen.blit(font_surface, (175, 50))

    draw_snake(cell1, cell4)
    draw_ladder(cell2, cell6)

    # Get the keys that are pressed
    key = pg.key.get_pressed()
    player.position = handle_key_press(key)

    # Check if the quit event is triggered
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.flip()
    clock.tick(60)
pg.quit()

