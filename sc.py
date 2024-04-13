import pygame as pg
import random as rd
from abc import ABC, abstractmethod
import numpy as np

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

# Utils
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

# Function to change the player position to the chosen cell position
def change_position_to_cell(cell):
    player.rect.topleft = cell.rect.topleft
    player.position = cell.position
    player.current_cell = cell
    return player.rect.topleft

# Function to draw the timer on the screen. value is the time in seconds.
def draw_timer(value=0):
    font = pg.font.Font(None, 15)  # Create a font object
    text_surface = font.render(f"Timer: {value}", True, (255, 255, 255))  # Create a surface with the text
    text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))  # Position the text at the top right corner of the screen
    screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen

# Function to draw the shortest distance on the screen. value is the minimum possible number of steps.
def draw_shortest_distance(value=0):
    font = pg.font.Font(None, 15)  # Create a font object
    text_surface = font.render(f"Minimum possible number of steps: {value}", True, (255, 255, 255))  # Create a surface with the text
    text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 20))  # Position the text at the top right corner of the screen
    screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen

# Function to draw the score on the screen. value is the score.
def draw_score(value=0):
    font = pg.font.Font(None, 15)  # Create a font object
    text_surface = font.render(f"Score: {value}", True, (255, 255, 255))  # Create a surface with the text
    text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 30))  # Position the text at the top right corner of the screen
    screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen


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
        font = pg.font.Font(None, 15)
        for i in range(1, len(self.cells_list)+1):
            # Update the surface (skin) of each cell on the screen
            screen.blit(self.cells_list[i].surface, self.cells_list[i].rect)
            # Render the text on each cell
            text_surface = font.render(str(i), False, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.cells_list[i].rect.center)
            screen.blit(text_surface, text_rect)
            
    def set_color(self, array):
        self.surface.fill(array)

def roll_dice():
    return rd.randint(1, 6)

class Entity(ABC):
    def __init__(self, start_cell=None, end_cell=None):
      # start_cell and end_cell are objects of the Cell class
        self.start_cell = start_cell
        self.end_cell = end_cell

    @abstractmethod
    def put_on_board(self):
        pass

    @abstractmethod
    def draw(self):
        pass

class Snake(Entity):
    def __init__(self, start_cell=None, end_cell=None):
        super().__init__(start_cell, end_cell)

    def put_on_board(self) -> None:
        # Check if the start and end cells are available for placement
        if self.start_cell.contents == None and self.end_cell.contents == None:
            # Place the snake on the start and end cells
            self.start_cell.contents = self
            self.end_cell.contents = self
        # Avoid placing the same start and end cells
        elif self.start_cell == self.end_cell:
            return
        else:
            return  

    def draw(self) -> None:
        # Draw only if the snake is placed
        if self.start_cell.contents != None and self.end_cell.contents != None and self.start_cell != self.end_cell:
            pg.draw.line(screen, (255, 0, 0), self.start_cell.rect.center, self.end_cell.rect.center, 5)

class Ladder(Entity):
    def __init__(self, start_cell=None, end_cell=None):
        super().__init__(start_cell, end_cell)
        self.start_cell = start_cell
        self.end_cell = end_cell

    def put_on_board(self) -> None:
        # Check if the start and end cells are available for placement
        if self.start_cell.contents == None and self.end_cell.contents == None:
            # Place the ladder on the start and end cells
            self.start_cell.contents = self
            self.end_cell.contents = self
        # Avoid placing the same start and end cells
        elif self.start_cell == self.end_cell:
            return
        else:
            return  

    def draw(self) -> None:
        # Draw only if the ladder is placed
        if self.start_cell.contents != None and self.end_cell.contents != None and self.start_cell != self.end_cell:
            pg.draw.line(screen, (0, 255, 0), self.start_cell.rect.center, self.end_cell.rect.center, 5)
            
class Generator():
    def __init__(self, rows: int, columns: int, board):
        self.rows = rows
        self.columns = columns
        self.cells_list = board.cells_list
        self.entity_matrices = []
        self.snakes_count = 0
        self.ladders_count = 0
        self.snakes_created = False
        self.ladders_created = False
        
    def board_cells_to_matrix(self) -> list:
        board_matrix = np.zeros((self.rows, self.columns), dtype=int)
        for key, value in self.cells_list.items():
            row = (key - 1) // self.columns
            column = (key - 1) % self.columns
            board_matrix[row, column] = key
        return np.flipud(board_matrix) 
    
    def create_null_matrices(self) -> list:
        # generate null matrices for entities with sizes 3x1 to 5x5
        null_matrices = []
        for i in range(3, 6): 
            for j in range(1, 6):
                null_matrices.append(np.zeros((i, j)))
        return null_matrices
    
    def put_entity_matrix(self, board_matrix, null_matrix, entity_type) -> bool:
        entity_rows, entity_columns = null_matrix.shape
        row_start = rd.randint(1, self.rows - entity_rows)
        column_start = rd.randint(1, self.columns - entity_columns)
        
        # check if the position is available
        if np.all(board_matrix[row_start: row_start + entity_rows, column_start: column_start + entity_columns] != 0):
            # add the extracted matrix to the list
            self.entity_matrices.append((board_matrix[row_start: row_start + entity_rows, column_start: column_start + entity_columns].copy(), entity_type)) 
            # place the null matrix
            board_matrix[row_start: row_start + entity_rows, column_start: column_start + entity_columns] = null_matrix
            
            # Update the count of snakes and ladders placed
            if entity_type == 'snake':
                self.snakes_count += 1
            elif entity_type == 'ladder':
                self.ladders_count += 1
                
            return True
        
        return False
    
    def smooth_placement(self) -> None:
        # cover approximately 50% of the board with entities
        board_matrix = self.board_cells_to_matrix()
        total_elements = board_matrix.size
        target_elements = int(total_elements * 0.5)
        null_matrices = self.create_null_matrices()
        rd.shuffle(null_matrices)
        
        elements_covered = 0
        for null_matrix in null_matrices:
            if elements_covered + null_matrix.size <= target_elements:
                # Determine the entity type based on the current counts
                if self.snakes_count <= self.ladders_count:
                    entity_type = 'snake'
                else:
                    entity_type = 'ladder'
                
                if self.put_entity_matrix(board_matrix, null_matrix, entity_type):
                    elements_covered += null_matrix.size
            else:
                break
    
    def get_entity_coordinates(self, entity_matrix) -> int:
        # get opposite corners of an entity matrix 
        rows, columns = entity_matrix.shape
        
        # entity is a straight line
        if columns == 1:
            top_corner = entity_matrix[0, 0]
            bottom_corner = entity_matrix[rows - 1, 0]
        
        # entity is a cube/rectangle   
        else:
            top_row = 0
            bottom_row = rows - 1
            
            # randomly select a column for a top corner
            selected_column = rd.choice([0, columns - 1])
            # randomly select corner from the top row
            top_corner = entity_matrix[top_row, selected_column]
            
            # ensure corners are taken from different columns
            if selected_column == 0:
                bottom_corner = entity_matrix[bottom_row, selected_column - 1]
            else:
                bottom_corner = entity_matrix[bottom_row, 0]
                
        return top_corner, bottom_corner
    
    def create_snakes(self) -> None:
        # ensure method is called only once
        if not self.snakes_created:
            self.smooth_placement()
            
            for entity_matrix, entity_type in self.entity_matrices:
                if entity_type == 'snake':
                    top_coordinate, bottom_coordinate = self.get_entity_coordinates(entity_matrix)
                    snake = Snake(start_cell=self.cells_list[top_coordinate], end_cell=self.cells_list[bottom_coordinate])
                    snake.put_on_board()
                    snake.draw()
                    
                    # snake1 = Snake(start_cell=board.cells_list[75], end_cell=board.cells_list[33])
            
            # block the method once it is called  
            self.snakes_created = True

    
    def create_ladders(self) -> None:
        # ensure method is called only once
        if not self.ladders_created:
            self.smooth_placement()
            
            for entity_matrix, entity_type in self.entity_matrices:
                if entity_type == 'ladder':
                    top_coordinate, bottom_coordinate = self.get_entity_coordinates(entity_matrix)
                    ladder = Ladder(start_cell=self.cells_list[bottom_coordinate], end_cell=self.cells_list[top_coordinate])
                    ladder.put_on_board()
                    ladder.draw()
            
            # block the method once it is called  
            self.ladders_created = True
  
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

class ProgressBar:
    def __init__(self, position, size, color=(255, 255, 255), bg_color=(100, 100, 100)):
        self.position = position
        self.size = size
        self.color = color
        self.bg_color = bg_color
        self.progress = 0  # Progress ranges from 0 to 1

    def update(self, progress):
        self.progress = progress

    def draw(self, screen):
        # Draw the background
        pg.draw.rect(screen, self.bg_color, (*self.position, *self.size))
        # Draw the progress bar
        pg.draw.rect(screen, self.color, (*self.position, self.size[0]*self.progress, self.size[1]))

board = Board(rows, columns)
board.set_color((255, 255, 255))
board.create_cells(generate_coordinates(rows, columns, cell_size))

player = Player(position=[255, 425])
player.set_color([200, 50, 50])
player.current_cell = board.cells_list[1]

progress_bar = ProgressBar((10, 10), (200, 20))

# Each frame is filled with black color, so that the previous frame is not visible
screen.fill((0, 0, 0))
# Draw the board surface on the screen
screen.blit(board.surface, (250, 150))
board.update_cells()
# Draw the player on the screen
screen.blit(player.surface, player.rect)
# Draw the font on the screen
screen.blit(font_surface, (175, 50))
# Draw the timer on the screen
draw_timer()
# Draw the shortest distance on the screen
draw_shortest_distance()
# Draw the score on the screen
draw_score()
# Generate snakes and ladders
generator = Generator(10, 10, board)
generator.create_snakes()
generator.create_ladders()

# Main game loop (same as main function)
running = True
while running:

    # # Each frame is filled with black color, so that the previous frame is not visible
    # screen.fill((0, 0, 0))
    # # Draw the board surface on the screen
    # screen.blit(board.surface, (250, 150))
    # board.update_cells()
    # # Draw the player on the screen
    # screen.blit(player.surface, player.rect)
    # # Draw the font on the screen
    # screen.blit(font_surface, (175, 50))
    # # Draw the timer on the screen
    # draw_timer()
    # # Draw the shortest distance on the screen
    # draw_shortest_distance()
    # # Draw the score on the screen
    # draw_score()
    # # Generate snakes and ladders
    # generator = Generator(10, 10, board)
    # generator.create_snakes()
    # generator.create_ladders()
    # Create and update the progress bar
    progress = player.current_cell.number / len(board.cells_list)
    progress_bar.update(progress)
    # Draw the updated progress bar on the screen
    progress_bar.draw(screen)

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