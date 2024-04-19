import pygame as pg
import random as rd
from abc import ABC, abstractmethod
import numpy as np
import time
from enum import Enum

# Initialize the pygame module with screen size, caption and color
pg.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Snakes and Ladders")

# Define the number of rows, columns, cell size and gap between cells
ROWS = 10
COLUMNS = 10
CELL_SIZE = 25
GAP = 5


class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PLAYER_COLOR = (200, 50, 50)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)


PLAYER_START_POSITION = [255, 425]

# Main game board class
class Board():
    """Represents the game board."""

    def __init__(self, rows: int, columns: int, cells_list={}, cell_size=CELL_SIZE, gap=GAP):
        self.rows = rows
        self.columns = columns
        self.cells_list = cells_list
        self.surface = pg.Surface((rows * (cell_size + gap) + gap, rows * (cell_size + gap) + gap))
        self.snakes = []
        self.ladders = []

    def create_cells(self, coordinates_array):
        """Creates the cells for the board."""
        number_of_cells_on_board = self.rows * self.columns
        # Create a dictionary of cells (cells_list) with their respective positions from the coordinates_array
        for i in range(1, number_of_cells_on_board + 1):
            coordinates = coordinates_array[i - 1]
            # Each cell is an object of the Cell class
            self.cells_list[i] = Cell(position=coordinates)
            self.cells_list[i].set_color(Color.BLACK.value)
            self.cells_list[i].number = i

    def update_cells(self):
        font = pg.font.Font(None, 15)
        for i in range(1, len(self.cells_list) + 1):
            # Update the surface (skin) of each cell on the screen
            screen.blit(self.cells_list[i].surface, self.cells_list[i].rect)
            # Render the text on each cell
            text_surface = font.render(str(i), False, Color.WHITE.value)
            text_rect = text_surface.get_rect(center=self.cells_list[i].rect.center)
            screen.blit(text_surface, text_rect)

    def set_color(self, array):
        self.surface.fill(array)


def roll_dice():
    return rd.randint(1, 6)


class Entity(ABC):
    """Represents an entity on the board."""

    def __init__(self, start_cell=None, end_cell=None, color=None):
        # start_cell and end_cell are objects of the Cell class
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.color = color

    @abstractmethod
    def put_on_board(self):
        """Places the entity on the board."""
        pass

    @abstractmethod
    def draw(self):
        """Draws the entity on the screen."""
        pass


class Snake(Entity):
    """Represents a snake on the board."""

    def __init__(self, start_cell=None, end_cell=None):
        super().__init__(start_cell, end_cell, Color.RED.value)

    def draw(self):
        """Draws the snake on the screen."""
        pg.draw.line(screen, self.color, self.start_cell.rect.center, self.end_cell.rect.center, 5)

    def put_on_board(self) -> None:
        """Places the snake on the board."""
        if self.start_cell.contents == None and self.end_cell.contents == None:
            self.start_cell.contents = self
            self.end_cell.contents = self


class Ladder(Entity):
    """Represents a ladder on the board."""

    def __init__(self, start_cell=None, end_cell=None):
        super().__init__(start_cell, end_cell, Color.GREEN.value)

    def draw(self):
        """Draws the ladder on the screen."""
        pg.draw.line(screen, self.color, self.start_cell.rect.center, self.end_cell.rect.center, 5)

    def put_on_board(self) -> None:
        """Places the ladder on the board."""
        if self.start_cell.contents == None and self.end_cell.contents == None:
            self.start_cell.contents = self
            self.end_cell.contents = self


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
            self.entity_matrices.append(
                board_matrix[row_start: row_start + entity_rows, column_start: column_start + entity_columns].copy())
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
    """
        This class is for objects player in the game
        score : the total score of the player
        entity encountered: boolean value whether the player reacted to the entity or not in each loop it will be False
        num_snakes: how many snakes the player encounters during the game (if 0 points will double in the end)
    """

    def __init__(self, position=[0, 0], current_cell=None, tot_score=100):
        self.surface = pg.Surface([CELL_SIZE, CELL_SIZE])
        self.rect = self.surface.get_rect()
        self.rect.topleft = position
        self.position = position
        self.current_cell = current_cell
        self.score = tot_score
        self.num_snakes = 0

    def set_position(self, array):
        self.position = array
        self.rect.topleft = array

    def set_color(self, array):
        self.surface.fill(array)

    # Score will update each time the player encounters an entity LADDER (+5) or SNAKE (-5)
    def react_to_entity(self, entity):
        if isinstance(entity, Snake):
            self.position = change_position_to_cell(self, entity.end_cell)
            self.snake_encountered()
            self.update_score(-5)
        elif isinstance(entity, Ladder):
            self.position = change_position_to_cell(self, entity.end_cell)
            self.update_score(+5)

    # A method to update the player's score during the game to for display in the end
    def update_score(self, points: int = 0):
        self.score += points
        return self.score

    # A method to keep count of how many snakes were encountered (bonus)
    def snake_encountered(self):
        self.num_snakes += 1
        return True


# The board consists of cells, which are the squares
class Cell():
    def __init__(self, size=[CELL_SIZE, CELL_SIZE], position=[0, 0], contents=None):
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
    def __init__(self, position, size, color=Color.WHITE.value, bg_color=(100, 100, 100)):
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
        pg.draw.rect(screen, self.color, (*self.position, self.size[0] * self.progress, self.size[1]))


class Timer:
    def __init__(self):
        self.start_time = time.time()

    def get_elapsed_time(self):
        # Return the elapsed time in seconds (int)
        return int(time.time() - self.start_time)

    def draw(self):
        font = pg.font.Font(None, 15)
        text_surface = font.render(f"Timer: {self.get_elapsed_time()}", True, Color.WHITE.value)
        text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(text_surface, text_rect)

    def reset(self):
        self.start_time = time.time()

# Function to generate the coordinates of the cells on the board
def generate_coordinates(rows:int, columns:int, cell_size:int, start_x:int=255, start_y:int=425) -> list[list[int]]:
    cells_coordinates = []
    gap = 5
    for row in range(rows):
        for col in range(columns):
            x = start_x + (cell_size + GAP) * col
            y = start_y - (cell_size + GAP) * row
            cells_coordinates.append([x, y])
    return cells_coordinates

# Function to change the player position to the chosen cell position
def change_position_to_cell(player:Player, cell:Cell) -> tuple[int, int]:
    player.rect.topleft = cell.rect.topleft
    player.position = cell.position
    player.current_cell = cell
    return player.rect.topleft

# Function to draw the shortest distance on the screen. value is the minimum possible number of steps.
def draw_shortest_distance(value:int=0) -> None:
    font = pg.font.Font(None, 15)  # Create a font object
    text_surface = font.render(f"Minimum possible number of steps: {value}", True, Color.WHITE.value)  # Create a surface with the text
    text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 20))  # Position the text at the top right corner of the screen
    screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen

# Function to draw the score on the screen. value is the score.
def draw_score(value:int=0) -> None:
    font = pg.font.Font(None, 15)  # Create a font object
    text_surface = font.render(f"Score: {value}", True, Color.WHITE.value)  # Create a surface with the text
    text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 30))  # Position the text at the top right corner of the screen
    screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen

# Function to draw the past games time on the screen. past_games_time is a list of times.
def draw_past_games_scores(past_games_scores:list[int]) -> None:
    font = pg.font.Font(None, 15)  # Create a font object
    y_position = 40
    # Sort the past games time in ascending order
    past_games_scores = quicksort(past_games_scores)
    for i, score in enumerate(past_games_scores):
        text_surface = font.render(f"Game {i+1} score: {score}", True, Color.WHITE.value)  # Create a surface with the text
        text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, y_position))  # Position the text at the top right corner of the screen
        screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen
        y_position += 10

def quicksort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x > pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x < pivot]
    return quicksort(left) + middle + quicksort(right)


# Create a font object to render the text on the screen
font = pg.font.Font(None, 36)
font_surface = font.render("Welcome to the Snakes and Ladders", False, Color.WHITE.value)
clock = pg.time.Clock()


def main():
    """Main game loop."""
    board = Board(ROWS, COLUMNS)
    board.set_color(Color.WHITE.value)
    board.create_cells(generate_coordinates(board.rows, board.columns, CELL_SIZE))

    player = Player(position=PLAYER_START_POSITION)
    player.set_color(Color.PLAYER_COLOR.value)
    player.current_cell = board.cells_list[1]

    progress_bar = ProgressBar((10, 10), (200, 20))
    timer = Timer()
    past_games_scores = []

    snake1 = Snake(start_cell=board.cells_list[75], end_cell=board.cells_list[33])
    snake1.put_on_board()
    board.snakes.append(snake1)

    ladder1 = Ladder(start_cell=board.cells_list[19], end_cell=board.cells_list[35])
    ladder1.put_on_board()
    board.ladders.append(ladder1)

    running = True
    while running:
        running = handle_events(player, board, timer, past_games_scores)
        if running:
            draw_game_state(player, board, timer, past_games_scores, board.snakes, board.ladders, progress_bar)
            update_game_state(player)

        # Update the display and set the frame rate
        pg.display.flip()
        clock.tick(60)
    # Quit the pygame module at the end
    pg.quit()


def handle_events(player, board, timer, past_games_scores):
    """Handles game events."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
        if event.type == pg.KEYDOWN:
            # If the key is the space bar
            if event.key == pg.K_SPACE:
                # Change the player position based on the dice roll
                moves = roll_dice()
                current_cell_number = player.current_cell.number
                next_cell_number = current_cell_number + moves
                # Ensure that the player does not move beyond the last cell
                if next_cell_number <= 100:
                    player.position = change_position_to_cell(player, board.cells_list[next_cell_number])
                else:
                    player.position = change_position_to_cell(player, board.cells_list[100])
                    # Special bonus (if player doesn't encounter any snakes score is doubled)
                    if player.num_snakes == 0:
                        player.update_score(player.score)
            # Reset button
            if event.key == pg.K_r:
                # Record the total score only if the player reaches the last cell
                if player.current_cell == board.cells_list[100]:
                    past_games_scores.append(player.update_score())
                player.position = change_position_to_cell(player, board.cells_list[1])
                player.update_score((-1 * player.score) + 100)
                timer.reset()
    return True


def update_game_state(player):
    if player.current_cell.contents is not None and player.current_cell == player.current_cell.contents.start_cell:
        player.react_to_entity(player.current_cell.contents)


def draw_game_state(player, board, timer, past_games_scores, snakes, ladders, progress_bar):
    """Draws the game state."""
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
    draw_score(player.score)
    # Draw the test snakes and ladders

    for snake in board.snakes:
        snake.draw()

    for ladder in board.ladders:
        ladder.draw()

    # Create and update the progress bar
    progress = player.current_cell.number / len(board.cells_list)
    progress_bar.update(progress)
    # Draw the updated progress bar on the screen
    progress_bar.draw(screen)
    draw_past_games_scores(past_games_scores)


if __name__ == "__main__":
    main()
