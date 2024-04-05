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

cells_coordinates = [
    [255, 155],
    [330, 155],
    [405, 155],
    [255, 230],
    [330, 230],
    [405, 230], 
    [255, 305],
    [330, 305],
    [405, 305]
]

# Create a font object to render the text
font = pg.font.Font(None, 36)
font_surface = font.render("Welcome to the Snakes and Ladders", False, "White")
clock = pg.time.Clock()

# Create a player rect with x, y, width, and height

class Board():
    def __init__(self, rows, columns, cells_list={}):
        self.rows = rows
        self.columns = columns
        self.cells_list = cells_list

    def create_cells(self, coordinates_array):
        number_of_cells = self.rows * self.columns
        for i in range(1, number_of_cells+1):
            coordinates = coordinates_array[i-1]
            self.cells_list[i] = Cell(position=coordinates)
            self.cells_list[i].set_color([0, 0, 0])

    def update_cells(self):
        for i in range(1, len(self.cells_list)+1):
            screen.blit(self.cells_list[i].surface, self.cells_list[i].rect)

class Entity():
    def __init__(self, start_cell=None, end_cell=None):
        self.start_cell = start_cell
        self.end_cell = end_cell

    def create(self, start_cell, end_cell):
        pass


class Cell():
    def __init__(self, surface=[70, 70], position=[0, 0]):
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


def handle_key_press(key):
    if key[pg.K_1]:
        player.position = change_position_to_cell(board.cells_list[1])
    elif key[pg.K_2]:
        player.position = change_position_to_cell(board.cells_list[2])
    elif key[pg.K_3]:
        player.position = change_position_to_cell(board.cells_list[3])
    elif key[pg.K_4]:
        player.position = change_position_to_cell(board.cells_list[4])
    elif key[pg.K_5]:
        player.position = change_position_to_cell(board.cells_list[5])
    elif key[pg.K_6]:
        player.position = change_position_to_cell(board.cells_list[6])
    elif key[pg.K_7]:
        player.position = change_position_to_cell(board.cells_list[7])
    elif key[pg.K_8]:
        player.position = change_position_to_cell(board.cells_list[8])
    elif key[pg.K_9]:
        player.position = change_position_to_cell(board.cells_list[9])
    return player.position

running = True
while running:

    # Fill the screen with black, so that the previous trail of the player rect is removed
    screen.fill((0, 0, 0))
    screen.blit(board_surface, (250, 150))

    board = Board(3, 3)
    board.create_cells(cells_coordinates)
    board.update_cells()

    screen.blit(player.surface, player.rect)
    
    screen.blit(font_surface, (175, 50))

    draw_snake(board.cells_list[1], board.cells_list[4])
    draw_ladder(board.cells_list[2], board.cells_list[6])

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

