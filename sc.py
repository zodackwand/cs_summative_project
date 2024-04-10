import pygame as pg
import random

# Initialize the pygame module with screen size, caption and color
pg.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Snakes and Ladders")

# Define the number of rows, columns, cell size and gap between cells
rows = 10
columns = 10
cell_size = 25
gap = 5

# Function to generate the coordinates of the cells on the board
def generate_coordinates(rows, columns, cell_size, start_x=255, start_y=425):
    cells_coordinates = []
    gap = 5
    for row in range(rows):
        for col in range(columns):
            x = start_x + (cell_size + gap) * col
            y = start_y - (cell_size + gap) * row
            cells_coordinates.append([x, y])
    return cells_coordinates

# Create a font object to render the text on the screen
font = pg.font.Font(None, 36)
font_surface = font.render("Welcome to the Snakes and Ladders", False, "White")
clock = pg.time.Clock()

# Main game board class
class Board():
    def __init__(self, rows: int, columns: int, cells_list={}):
        self.rows = rows
        self.columns = columns
        self.cells_list = cells_list
        self.surface = pg.Surface((rows * (cell_size + gap) + gap, rows * (cell_size+ gap) + gap))

    def create_cells(self, coordinates_array):
        number_of_cells_on_board = self.rows * self.columns
        # Create a dictionary of cells (cells_list) with their respective positions from the coordinates_array
        for i in range(1, number_of_cells_on_board+1):
            coordinates = coordinates_array[i-1]
            # Each cell is an object of the Cell class
            self.cells_list[i] = Cell(position=coordinates)
            self.cells_list[i].set_color([0, 0, 0])
            self.cells_list[i].number = i

    def update_cells(self):
        for i in range(1, len(self.cells_list)+1):
            # Update the surface (skin) of each cell on the screen
            screen.blit(self.cells_list[i].surface, self.cells_list[i].rect)

    def set_color(self, array):
        self.surface.fill(array)

def generate_snakes(number_of_snakes: int):
    # Use put_on_board() method to put the snakes on the board
    # Ruslan's script
    pass

def generate_ladders(number_of_ladders: int):
    # Use put_on_board() method to put the ladders on the board
    # Ruslan's script
    pass

def roll_dice():
    return random.randint(1, 6)

class Entity():
    def __init__(self, start_cell=None, end_cell=None):
        # start_cell and end_cell are objects of the Cell class
        self.start_cell = start_cell
        self.end_cell = end_cell

    def put_on_board(self, start_cell, end_cell):
        pass

    def draw(self):
        pass
        
class Snake(Entity):
    def __init__(self, start_cell=None, end_cell=None):
        super().__init__(start_cell, end_cell)
        self.start_cell = start_cell
        self.end_cell = end_cell
    def put_on_board(self):
        self.start_cell.contents = self
        self.end_cell.contents = self
    def draw(self):
        pg.draw.line(screen, (255, 0, 0), self.start_cell.rect.center, self.end_cell.rect.center, 5)


class Ladder(Entity):
    def __init__(self, start_cell=None, end_cell=None):
        super().__init__(start_cell, end_cell)
        self.start_cell = start_cell
        self.end_cell = end_cell
    def put_on_board(self):
        self.start_cell.contents = self
        self.end_cell.contents = self
    def draw(self):
        pg.draw.line(screen, (0, 255, 0), self.start_cell.rect.center, self.end_cell.rect.center, 5)

class Player():
    def __init__(self, position=[0, 0], current_cell=None):
        self.surface = pg.Surface([cell_size, cell_size])
        self.rect = self.surface.get_rect()
        self.rect.topleft = position
        self.position = position
        self.current_cell = current_cell

    def set_position(self, array):
        self.position = array
        self.rect.topleft = array

    def set_color(self, array):
        self.surface.fill(array)

    def react_to_entity(self, entity):
       player.position = change_position_to_cell(entity.end_cell)

# The board consists of cells, which are the squares
class Cell():
    def __init__(self, size=[cell_size, cell_size], position=[0, 0], contents=None):
        self.surface = pg.Surface(size)
        self.rect = self.surface.get_rect()
        self.rect.topleft = position
        self.position = position
        self.contents = contents
        self.number = None

    def set_color(self, array):
        self.surface.fill(array)

    def set_position(self, array):
        self.position = array
        self.rect.topleft = array

# Function to change the player position to the chosen cell position
def change_position_to_cell(cell):
    player.rect.topleft = cell.rect.topleft
    player.position = cell.position
    player.current_cell = cell
    return player.rect.topleft


board = Board(rows, columns)
board.set_color((255, 255, 255))
board.create_cells(generate_coordinates(rows, columns, cell_size))

player = Player(position=[255, 425])
player.set_color([200, 50, 50])
player.current_cell = board.cells_list[1]

# Main game loop (same as main function)
running = True
while running:

    # Each frame is filled with black color, so that the previous frame is not visible
    screen.fill((0, 0, 0))
    # Draw the board surface on the screen
    screen.blit(board.surface, (250, 150))
    board.update_cells()
    # Draw the player on the screen
    screen.blit(player.surface, player.rect)
    # Draw the font on the screen
    screen.blit(font_surface, (175, 50))
    # Draw the test snakes and ladders
    snake1 = Snake(start_cell=board.cells_list[75], end_cell=board.cells_list[33])
    snake1.draw()
    snake1.put_on_board()
    ladder1 = Ladder(start_cell=board.cells_list[19], end_cell=board.cells_list[35])
    ladder1.draw()
    ladder1.put_on_board()

    if player.current_cell.contents != None:
        player.react_to_entity(player.current_cell.contents)
    

    # Check if the quit event is triggered
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            # If the key is the space bar
            if event.key == pg.K_SPACE:
                # Change the player position based on the dice roll
                current_cell_number = player.current_cell.number
                next_cell_number = current_cell_number + roll_dice()
                # Ensure that the player does not move beyond the last cell
                if next_cell_number <= 100:
                    player.position = change_position_to_cell(board.cells_list[next_cell_number])
                else:
                    player.position = change_position_to_cell(board.cells_list[100])

    # Update the display and set the frame rate
    pg.display.flip()
    clock.tick(60)
# Quit the pygame module at the end
pg.quit()