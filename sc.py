import pygame as pg
import random as rd
from abc import ABC, abstractmethod
import numpy as np
import time

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

# Function to change the player position to the chosen cell position
def change_position_to_cell(cell):
    player.rect.topleft = cell.rect.topleft
    player.position = cell.position
    player.current_cell = cell
    return player.rect.topleft

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

# Function to draw the past games time on the screen. past_games_time is a list of times.
def draw_past_games_time(past_games_time):
    font = pg.font.Font(None, 15)  # Create a font object
    y_position = 40
    # Sort the past games time in ascending order
    past_games_time = quicksort(past_games_time)
    for i, time in enumerate(past_games_time):
        text_surface = font.render(f"Game {i+1} time: {time}", True, (255, 255, 255))  # Create a surface with the text
        text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, y_position))  # Position the text at the top right corner of the screen
        screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen
        y_position += 10

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


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
    def __init__(self, rows: int, columns: int, cells_list={}):
        self.rows = rows
        self.columns = columns
        self.cells_list = cells_list
        self.entity_matrices = []
        
    def board_cells_to_matrix(self) -> list:
        board_matrix = np.zeros((self.rows, self.columns), dtype=int)
        for key, value in input_dict.items():
            row = (key - 1) // self.columns
            column = (key - 1) % self.columns
            board_matrix[row, column] = key
        return np.flipud(board_matrix) 
    
    def create_null_matrices(self) -> list:
        # generate null matrices for entities with sizes 3x1 to 4x4
        null_matrices = []
        for i in range(3, 5): 
            for j in range(1, 5):
                null_matrices.append(np.zeros((i, j)))
        return null_matrices
    
    def put_entity_matrix(self, board_matrix, null_matrix) -> bool:
        entity_rows, entity_columns = null_matrix.shape
        row_start = rd.randint(0, self.rows - entity_rows)
        column_start = rd.randint(0, self.columns - entity_columns)
        
        # check if the position is availible
        if np.all(board_matrix[row_start: row_start + entity_rows, column_start: column_start + entity_columns] != 0):
            # add the extracted matrix to the list
            self.entity_matrices.append(board_matrix[row_start: row_start + entity_rows, column_start: column_start + entity_columns].copy()) 
            # place the null matrix
            board_matrix[row_start: row_start + entity_rows, column_start: column_start + entity_columns] = null_matrix
            return True
        
        return False
    
    def smooth_placement(self) -> None:
        # Entities cover approx. 50% of the board
        pass
    
    def get_entity_coordinates(self) -> list:
        pass
    
    def create_snakes(self):
        pass
    
    def create_ladders(self):
        pass
  
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

class Timer:
    def __init__(self):
        self.start_time = time.time()
    def get_elapsed_time(self):
        # Return the elapsed time in seconds (int)
        return int(time.time() - self.start_time)
    def draw(self):
        font = pg.font.Font(None, 15)
        text_surface = font.render(f"Timer: {self.get_elapsed_time()}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(text_surface, text_rect)
    def reset(self):
        self.start_time = time.time()


board = Board(rows, columns)
board.set_color((255, 255, 255))
board.create_cells(generate_coordinates(rows, columns, cell_size))

player = Player(position=[255, 425])
player.set_color([200, 50, 50])
player.current_cell = board.cells_list[1]

progress_bar = ProgressBar((10, 10), (200, 20))
timer = Timer()
past_games_time = []

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
    # Draw the timer on the screen
    timer.draw()
    # Draw the shortest distance on the screen
    draw_shortest_distance()
    # Draw the score on the screen
    draw_score()
    # Draw the test snakes and ladders
    snake1 = Snake(start_cell=board.cells_list[75], end_cell=board.cells_list[33])
    snake1.draw()
    snake1.put_on_board()
    ladder1 = Ladder(start_cell=board.cells_list[19], end_cell=board.cells_list[35])
    ladder1.draw()
    ladder1.put_on_board()
    # Create and update the progress bar
    progress = player.current_cell.number / len(board.cells_list)
    progress_bar.update(progress)
    # Draw the updated progress bar on the screen
    progress_bar.draw(screen)
    draw_past_games_time(past_games_time)

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
            # Reset button
            if event.key == pg.K_r:
                # Record the time taken if only the player reaches the last cell
                if player.current_cell == board.cells_list[100]:
                    past_games_time.append(timer.get_elapsed_time())
                player.position = change_position_to_cell(board.cells_list[1])
                timer.reset()


    # Update the display and set the frame rate
    pg.display.flip()
    clock.tick(60)
# Quit the pygame module at the end
pg.quit()