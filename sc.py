# Created by 5590073
try:
    import pygame as pg
    import random as rd
    from abc import ABC, abstractmethod
    import numpy as np
    import time
    from enum import Enum
    from collections import deque
    import os
    import logging
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you have installed the required libraries from our user guide!")
    print("You can install the required libraries using the command: !pip install library_name in a code cell.")
    os._exit(0)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Initialize the pygame module with screen size, caption and color
# Created by 5590073
try:
    pg.init()
except pg.error as e:
    print(f"Error initializing pygame: {e}")
    print("Make sure you have installed pygame!")
    os._exit(0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Snakes and Ladders")

# Define the number of rows, columns, cell size and gap between cells
# Created by 5590073
ROWS = 10
COLUMNS = 10
CELL_SIZE_PIXELS = 25
GAP_PIXELS = 5

# Defines an enumeration Color that represents different colors using RGB
# Created by 5590073
class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PLAYER_COLOR = (200, 50, 50)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)


PLAYER_START_POSITION = [255, 425]


# Main game board class
# Created by 5590073 and 5588113
class Board():
    """Represents the game board.

    Attributes:
        rows (int): The number of rows in the board.
        columns (int): The number of columns in the board.
        cells_list (dict): A dictionary of cells with their respective positions.
        surface (pygame.Surface): The surface representing the board.
        snakes (list): A list of Snake objects on the board.
        ladders (list): A list of Ladder objects on the board.
        shortest_distance (int): The shortest distance between the start cell and end cell.
    """
    # Created by 5590073
    def __init__(self, rows: int, columns: int, cells_list={}, cell_size=CELL_SIZE_PIXELS, gap=GAP_PIXELS):
        logging.info('Initializing Board')
        self.rows = rows
        self.columns = columns
        self.cells_list = cells_list
        self.surface = pg.Surface((rows * (cell_size + gap) + gap, rows * (cell_size + gap) + gap))
        self.snakes = []
        self.ladders = []
        self.shortest_distance = None
    # Created by 5590073
    def create_cells(self, coordinates_array) -> None:
        """
        Creates the cells for the board.

        coordinates_array: An array of coordinates for the cells.
        """
        logging.info('Creating cells')
        number_of_cells_on_board = self.rows * self.columns
        # Create a dictionary of cells (cells_list) with their respective positions from the coordinates_array
        for i in range(1, number_of_cells_on_board + 1):
            coordinates = coordinates_array[i - 1]
            # Each cell is an object of the Cell class
            self.cells_list[i] = Cell(position=coordinates)
            self.cells_list[i].set_color(Color.BLACK.value)
            self.cells_list[i].number = i
    # Created by 5590073
    def update_cells(self) -> None:
        """
        Updates the cells on the board. This includes updating the surface of each cell and rendering the text on each cell.
        """
        font = pg.font.Font(None, 15)
        for i in range(1, len(self.cells_list) + 1):
            # Update the surface (skin) of each cell on the screen
            screen.blit(self.cells_list[i].surface, self.cells_list[i].rect)
            # Render the text on each cell
            text_surface = font.render(str(i), False, Color.WHITE.value)
            text_rect = text_surface.get_rect(center=self.cells_list[i].rect.center)
            screen.blit(text_surface, text_rect)
    # Created by 5590073
    def set_color(self, color_array) -> None:
        """
        Sets the color of the board.

        color_array: An array representing the color.
        """
        self.surface.fill(color_array)
    
    # Created by 5588113  
    def create_board_graph(self) -> dict:
        """Create a graph representing connections between cells.

        The graph is stored in the board object.

        return: A dictionary representing the graph.
        """
        logging.info('Creating board graph')
        board_graph = {}
        for cell_number, cell in self.cells_list.items():
            board_graph[cell_number] = []
            # If ladder detected and node is not an end_cell, append ladder's end to the node
            if cell.contents is not None and isinstance(cell.contents, Ladder) and cell_number != cell.contents.end_cell.number:
                board_graph[cell_number].append(cell.contents.end_cell.number)
            else:
                for i in range(1, 7):  # Possible dice roll values
                    next_cell_number = cell_number + i
                    if next_cell_number <= 100:
                        if self.cells_list[next_cell_number].contents is not None:
                            next_cell_number = self.cells_list[next_cell_number].contents.end_cell.number
                        board_graph[cell_number].append(next_cell_number)
        self.board_graph = board_graph  # Store board graph in the board object
        return board_graph

    # Created by 5588113
    def calculate_shortest_path(self, start_cell_number: int, end_cell_number: int) -> None:
        """Calculate the shortest path between two cells using BFS."""
        if self.board_graph is None:
            raise ValueError("Board graph not initialized. Call create_board_graph() first.")

        visited = set()
        queue = deque([(start_cell_number, 0)])  # (cell_number, distance)
        while queue:
            cell_number, distance = queue.popleft()
            if cell_number == end_cell_number:
                self.shortest_distance = distance
                return
            visited.add(cell_number)
            for neighbor_cell in self.board_graph[cell_number]:
                if neighbor_cell not in visited:
                    queue.append((neighbor_cell, distance + 1))
        return # No path found


# Created by 5590073
def roll_dice():
    return rd.randint(1, 6)


# Created by 5590073 and 5588113
class Entity(ABC):
    """Represents an entity on the board."""

    def __init__(self, start_cell=None, end_cell=None, color=None):
        # start_cell and end_cell contain the same object of the Cell class
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


# Created by 5590073 and 5588113
class Snake(Entity):
    """Represents a snake on the board."""

    def __init__(self, start_cell=None, end_cell=None):
        super().__init__(start_cell, end_cell, Color.RED.value)

    def draw(self):
        """Draws the snake on the screen."""
        pg.draw.line(screen, self.color, self.start_cell.rect.center, self.end_cell.rect.center, 5)

    def put_on_board(self) -> bool:
        """Places the snake on the board."""
        # Check if the start and end cells are empty and not the same
        if self.start_cell.contents == None and self.end_cell.contents == None and self.start_cell != self.end_cell:
            self.start_cell.contents = self
            self.end_cell.contents = self
            return True

        return False


# Created by 5590073 and 5588113
class Ladder(Entity):
    """Represents a ladder on the board."""

    def __init__(self, start_cell=None, end_cell=None):
        super().__init__(start_cell, end_cell, Color.GREEN.value)

    def draw(self):
        """Draws the ladder on the screen."""
        pg.draw.line(screen, self.color, self.start_cell.rect.center, self.end_cell.rect.center, 5)

    def put_on_board(self) -> bool:
        """Places the ladder on the board."""
        # Check if the start and end cells are empty and not the same
        if self.start_cell.contents == None and self.end_cell.contents == None and self.start_cell != self.end_cell:
            self.start_cell.contents = self
            self.end_cell.contents = self
            return True

        return False


# Created by 5588113
class Generator:
    """This class manages the creation of snakes and ladders on the game board. It controls the percentage of the board
        covered with entities and shapes their placement to keep the player engaged while maintaining randomness.
        
        E.g. preventing creation of entities that are too long or placed horizontally.
    """
    
    def __init__(self, board: Board):
        """Initialize the Generator.
        
        Args:
            board (Board): The class Board attribute
            
        Attributes:
            rows (int): Number of rows in the game board.
            columns (int): Number of columns in the game board.
            entity_matrices (list): A list to store matrices that incluede cells on which the entities are placed.
            
        Data structures:
            Dictionary/Hashmap
            List/Array
            2D List (matrix)
                
        Methods:
            _board_cells_to_matrix (protected): Converts the class Board's cells to a matrix.
            _create_null_matrices (protected): Creates a set of null matrices ranging from 3x2 to 5x5 that reserve spaces for entities.
            _put_null_matrix (protected): Indicates, whether a specific place can be reserved for an entity.
            _smooth_placement (protected): Controls the entities coverage.
            _get_entities_coordinates (protected): Get values of opposite corners from entity matrices
            
            create_snakes_on_board (public): Receive coordinates for snakes and asign them with class Cell
            create_ladders_on_board (pulic): Receive coordinates for ladders and asign them with class Cell
            
        Example private methods procedure:
        
            Board matrix (10x10), null matrices placed:

                [[ 91  92  93  94  95  96  97  98  99 100]
                [ 81  82  83  84  85  86  87  88  89  90]
                [ 71  72   0   0   0  76  77  78  79  80]
                [ 61  62   0   0   0  66  67  68  69   0]
                [ 51  52   0   0   0  56  57  58  59   0]
                [ 41  42   0   0   0   0   0  48  49   0]
                [ 31  32  33  34  35   0   0  38  39  40]
                [ 21  22   0   0   0   0   0  28  29  30]
                [ 11  12   0   0   0  16  17  18  19  20]
                [  1   2   0   0   0   6   7   8   9  10]]

            Extracted entity Matrices according to null matrices positions:
            
                [ 75 ]   [ 70 ]   [ 23  24  25 ]   [ 73  74 ]   [ 46  47 ]
                [ 65 ]   [ 60 ]   [ 13  14  15 ]   [ 63  64 ]   [ 36  37 ]
                [ 55 ]   [ 50 ]   [  3   4   5 ]   [ 53  54 ]   [ 26  27 ]
                [ 45 ]                             [ 43  44 ]
            
            Extracted coordinates list: [[45, 75], [50, 70], [5, 23] [43, 74], [26, 47]]
        """
        self.board = board
        self.rows = board.rows
        self.columns = board.columns
        self.entity_matrices = []

    def _board_cells_to_matrix(self) -> np.ndarray:
        """
        Convert board cells to a matrix.

        Returns:
            np.ndarray: The matrix representing the board cells.
        """
        # Called by: _smooth_placement()
        board_matrix = np.zeros((self.rows, self.columns), dtype=int)
        for key, value in self.board.cells_list.items():
            row = (key - 1) // self.columns
            column = (key - 1) % self.columns
            board_matrix[row, column] = key
        return np.flipud(board_matrix)

    def _create_null_matrices(self) -> list:
        """
        Create a set of null matrices ranging from 3x2 to 5x5 that reserve spaces for entities.
        
        Returns:
            list: A list of null matrices.
        """
        # Called by: _smooth_placement()
        null_matrices = []
        for i in range(3, 6):
            for j in range(2, 6):
                null_matrices.append(np.zeros((i, j)))
        return null_matrices

    def _put_null_matrix(self, board_matrix, null_matrix) -> bool:
        """
        Indicates whether a specific place can be reserved for an entity.

        Args:
            board_matrix (np.ndarray): The current state of the board matrix.
            null_matrix (np.ndarray): The null matrix representing the entity to be placed.

        Returns:
            bool: True if the entity can be placed, False otherwise.
        """
        # Called by: _smooth_placement()
        entity_rows, entity_columns = null_matrix.shape
        row_start = rd.randint(0, self.rows - entity_rows)
        column_start = rd.randint(0, self.columns - entity_columns)
        restricted_cells = [0, 1, self.rows * self.columns]

        selected_cells = board_matrix[row_start: row_start + entity_rows, column_start: column_start + entity_columns]
        # Avoid placing null matrix on start/end cell and on other null matrices
        if np.all(selected_cells != 0) and not np.any(np.isin(selected_cells, restricted_cells)):
            # Form entitiy matrix and put it in the list if placed succesfully
            self.entity_matrices.append(selected_cells.copy())
            board_matrix[row_start: row_start + entity_rows, column_start: column_start + entity_columns] = null_matrix
            return True 

        return False 

    def _smooth_placement(self) -> None:
        """
        Controls the entities coverage by adjusting the coverage percentage.

        This method is called by:
            - _get_entities_coordinates()
        """
        # Called by: create_snakes_on_board(), create_ladders_on_board()
        board_matrix = self._board_cells_to_matrix()
        total_elements = board_matrix.size
        # Ensure 70% coverage
        target_elements = int(total_elements * 0.7)
        null_matrices = self._create_null_matrices()
        rd.shuffle(null_matrices)

        elements_covered = 0
        for null_matrix in null_matrices:
            if elements_covered + null_matrix.size <= target_elements:
                if self._put_null_matrix(board_matrix, null_matrix):
                    elements_covered += null_matrix.size
            else:
                break

    def _get_entities_coordinates(self) -> list:
        """
        Get values of opposite corners from entity matrices.

        Returns:
            list: A list containing coordinates of entities' corners.
        """
        entities_coordinates = []
        self._smooth_placement()

        for entity_matrix in self.entity_matrices:
            rows, columns = entity_matrix.shape

            if columns == 1:
                # Get the top and bottom corner coordinates for entities with single column
                top_corner = entity_matrix[0, 0]
                bottom_corner = entity_matrix[rows - 1, 0]
            else:
                # For entities with multiple columns, select a random column for the top corner
                top_row = 0
                bottom_row = rows - 1
                selected_column = rd.choice([0, columns - 1])
                top_corner = entity_matrix[top_row, selected_column]

                # Depending on the selected column, get the corresponding bottom corner coordinate
                if selected_column == 0:
                    bottom_corner = entity_matrix[bottom_row, selected_column - 1]
                else:
                    bottom_corner = entity_matrix[bottom_row, 0]

            entities_coordinates.append([bottom_corner, top_corner])

        return entities_coordinates
    
    def create_snakes_on_board(self, board: Board) -> None:
        """
        Create snakes on the game board based on the coordinates obtained from _get_entities_coordinates.

        Args:
            board (Board): The game board where the snakes will be placed.
        """
        logging.info('Creating snakes on the game board')
        snakes_coordinates = self._get_entities_coordinates
        for cells in self._get_entities_coordinates():
            bottom_coordinate, top_coordinate = cells
            
            snake = Snake(start_cell=board.cells_list[top_coordinate], end_cell=board.cells_list[bottom_coordinate])
            if snake.put_on_board():
                board.snakes.append(snake)

    def create_ladders_on_board(self, board: Board) -> None:
        """
        Create ladders on the game board based on the coordinates obtained from _get_entities_coordinates.

        Args:
            board (Board): The game board where the ladders will be placed.
        """
        logging.info('Creating ladders on the game board')
        for cells in self._get_entities_coordinates():
            bottom_coordinate, top_coordinate = cells
            
            ladder = Ladder(start_cell=board.cells_list[bottom_coordinate], end_cell=board.cells_list[top_coordinate])
            if ladder.put_on_board():
                board.ladders.append(ladder)



# Created by 5590073, edited by 5555194
class Player():
    """
        Represents the player on the board

        _score : the total score of the player (private)
        num_snakes: how many snakes the player encounters during the game (if 0 points will double in the end)
        moves: will later be the dice value when rolled
        number_steps_made: how many steps the player has made
        history_stack: a stack to keep track of the player's move history
        rect: the rectangle representing the player
        rect.topleft: the top left corner of the rectangle (for positining)
        surface: the surface representing the player (like a skin)
    """

    # Created by 5590073 edited by 5555194
    def __init__(self, position=[0, 0], current_cell=None, tot_score=100, moves=0):
        self.surface = pg.Surface([CELL_SIZE_PIXELS, CELL_SIZE_PIXELS])
        self.rect = self.surface.get_rect()
        self.rect.topleft = position
        self.position = position
        self.current_cell = current_cell
        self._score = tot_score
        self.moves = moves
        self.num_snakes = 0
        self.number_steps_made = 0
        self.history_stack = []
    # Created by 5590073
    def set_position(self, position_array):
        self.position = position_array
        self.rect.topleft = position_array
    # Created by 5590073
    def set_color(self, color_array):
        self.surface.fill(color_array)

    def undo(self):
        """
        Undo the last move made by the player.
        """
        if self.history_stack:
            # Restore the previous state including position, score, moves, number of steps made, number of snakes encountered and current cell
            self.position, self._score, self.moves, self.number_steps_made, self.num_snakes, self.current_cell = self.history_stack.pop()
            self.rect.topleft = self.position

    # Created by 5555194 and 5590073
    # Score will update each time the player encounters an entity
    def react_to_entity(self, entity) -> None:
        logging.info('Player reacting to entity')
        if isinstance(entity, Snake):
            self.position = change_position_to_cell(self, entity.end_cell)
            self.snake_encountered()
            self.update_score(-5)
        elif isinstance(entity, Ladder):
            self.position = change_position_to_cell(self, entity.end_cell)
            self.update_score(+5)
        return None
    # Created by 5555194
    # A method to get the player's score
    def get_score(self) -> int:
        return self._score
    # Created by 5555194
    # A method to update the player's score during the game to for display in the end
    def update_score(self, points: int = 0) -> int:
        logging.info('Updating Player score')
        self._score += points
        return self._score
    # Created by 5555194
    # A method to keep count of how many snakes were encountered (bonus)
    def snake_encountered(self) -> None:
        logging.info('Player encountered a snake')
        self.num_snakes += 1
        return None
    # Created by 5555194
    # A method to reset the num_snakes variable back to zero
    def reset_num_snakes(self) -> None:
        logging.info('Resetting number of snakes encountered')
        self.num_snakes = 0
        return None
    # Created by 5555194
    # A method to reset the player's score back to 100
    def reset_score(self) -> None:
        logging.info('Resetting Player score')
        self._score = 100
        return None


# The board consists of cells, which are the squares
# Created by 5590073
class Cell():
    """
    Represents a cell on the game board.

    Attributes:
        surface (pygame.Surface): The surface representing the cell.
        rect (pygame.Rect): The rectangle representing the cell.
        position (list): The position of the cell on the board.
        contents (Entity): The entity (if any) contained in the cell.
        number (int): The number of the cell.
        size: The size of the cell in pixels.
    """
    def __init__(self, size=[CELL_SIZE_PIXELS, CELL_SIZE_PIXELS], position=[0, 0], contents=None):
        """
        Initializes the Cell with the given size, position, and contents.
        """
        self.surface = pg.Surface(size)
        self.rect = self.surface.get_rect()
        self.rect.topleft = position
        self.position = position
        self.contents = contents
        self.number = None

    def set_color(self, color_array):
        """
        Sets the color of the cell.

        color_array: An array representing the color.
        """
        self.surface.fill(color_array)

    def set_position(self, position_array):
        """
        Sets the position of the cell.

        position_array: An array representing the position.
        """
        self.position = position_array
        self.rect.topleft = position_array


# Created by 5590073
class ProgressBar:
    """
    Represents a progress bar in the game.

    Attributes:
        position (tuple): The position of the progress bar on the screen.
        size (tuple): The size of the progress bar.
        color (tuple): The color of the progress bar.
        bg_color (tuple): The background color of the progress bar.
        progress (float): The current progress, ranging from 0 to 1.
    """
    def __init__(self, position, size, color=Color.WHITE.value, bg_color=(100, 100, 100)):
        self.position = position
        self.size = size
        self.color = color
        self.bg_color = bg_color
        self.progress = 0  # Progress ranges from 0 to 1

    def update(self, progress):
        """
        Updates the progress of the progress bar.

        progress: The new progress, ranging from 0 to 1.
        """
        self.progress = progress

    def draw(self, screen):
        """
        Draws the progress bar on the screen.

        screen: The pygame.Surface object representing the screen.
        """
        # Draw the background
        # * unpacks the tuple into individual arguments
        pg.draw.rect(screen, self.bg_color, (*self.position, *self.size))
        # Draw the progress bar
        pg.draw.rect(screen, self.color, (*self.position, self.size[0] * self.progress, self.size[1]))


# Created by 5590073
class Timer:
    """
    Represents a timer in the game using time library.

    Attributes:
        start_time (float): The start time of the timer.
    """
    def __init__(self):
        self.start_time = time.time()

    def get_elapsed_time(self):
        """
        Returns the elapsed time since the timer was started.

        The elapsed time in seconds (int).
        """
        # Return the elapsed time in seconds (int)
        return int(time.time() - self.start_time)

    def draw(self):
        """
        Draws the timer on the screen.
        """
        font = pg.font.Font(None, 15)
        text_surface = font.render(f"Timer: {self.get_elapsed_time()}", True, Color.WHITE.value)
        text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(text_surface, text_rect)

    def reset(self):
        """
        Resets the timer to the current time.
        """
        self.start_time = time.time()


# Created by 5590073
def generate_coordinates(rows: int, columns: int, cell_size: int, start_x: int = 255, start_y: int = 425) -> list[list[int]]:
    """
    Generates a list of coordinates for a grid of cells.

    The function calculates the x and y coordinates for each cell in a grid, given the number of rows and columns,
    the size of each cell, and the starting x and y coordinates. The coordinates are calculated in pixels.

    rows: The number of rows in the grid.
    columns: The number of columns in the grid.
    cell_size: The size of each cell in pixels.
    start_x: The x-coordinate of the start in the grid. Defaults to 255.
    start_y: The y-coordinate of the start in the grid. Defaults to 425.
    return: A list of [x, y] coordinates for each cell in the grid.
    """
    logging.info('Generating coordinates')
    cells_coordinates = []
    for row in range(rows):
        for col in range(columns):
            x = start_x + (cell_size + GAP_PIXELS) * col
            y = start_y - (cell_size + GAP_PIXELS) * row
            cells_coordinates.append([x, y])
    return cells_coordinates

# Created by 5590073
def change_position_to_cell(player: Player, cell: Cell) -> tuple[int, int]:
    """
    Changes the position of the player to the position of a specified cell.

    This function updates the player's rectangle's top-left position, the player's position attribute, 
    and the player's current cell attribute to match the specified cell.

    player: The Player object whose position is to be changed.
    cell: The Cell object to which the player's position is to be changed.
    return: A tuple representing the new top-left position of the player's rectangle.
    """
    # Save the current state of the player before moving to a new cell
    player.history_stack.append((player.position, player._score, player.moves, player.number_steps_made, player.num_snakes, player.current_cell))
    player.number_steps_made += 1
    # Move the player to the new cell
    player.rect.topleft = cell.rect.topleft
    player.position = cell.position
    player.current_cell = cell
    return player.rect.topleft

# Created by 5590073
def draw_shortest_distance(value: int = 0) -> None:
    """
    Draws the shortest possible number of steps from start to end.

    This function creates a text surface with the minimum possible number of steps, 
    positions it at the top right corner of the screen, and then blits this surface onto the screen.

    value: The minimum possible number of steps. Defaults to 0.
    """
    font = pg.font.Font(None, 15)  # Create a font object
    text_surface = font.render(f"Minimum possible number of steps: {value}", True,
                               Color.WHITE.value)  # Create a surface with the text
    text_rect = text_surface.get_rect(
        topright=(SCREEN_WIDTH - 10, 20))  # Position the text at the top right corner of the screen
    screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen


# Created by 5590073
def draw_score(value: int = 0) -> None:
    """
    Draws the current score on the screen.

    This function creates a text surface with the current score, positions it at the top right corner of the screen, 
    and then blits this surface onto the screen.

    The current score. Defaults to 0.
    """
    font = pg.font.Font(None, 15)  # Create a font object
    text_surface = font.render(f"Score: {value}", True, Color.WHITE.value)  # Create a surface with the text
    text_rect = text_surface.get_rect(
        topright=(SCREEN_WIDTH - 10, 30))  # Position the text in the top right corner of the screen
    screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen


# Created by 5555194
def draw_dice_value(value: int = 0) -> None:
    """
    Draws the current dice value on the screen.

    This function creates a text surface with the current dice value, positions it at the middle of the screen, 
    and then blits this surface onto the screen.

    value: The current dice value. Defaults to 0.
    """
    font = pg.font.Font(None, 20)  # Create a font object
    text_surface = font.render(f"Press SPACE to roll the dice: {value}", True,
                               Color.WHITE.value)  # Create a surface with the text
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 180))  # Position the text at the mid right
    screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen
    return None

# Created by 5590073
def draw_number_steps_made(player) -> None:
    """
    Draws the number of steps made by the player on the screen.

    This function creates a text surface with the number of steps made by the player, positions it at the left of the screen, 
    and then blits this surface onto the screen.

    player: The Player object representing the player.
    """
    font = pg.font.Font(None, 15)  # Create a font object
    text_surface = font.render(f"Number of steps made: {player.number_steps_made}", True,
                               Color.WHITE.value)  # Create a surface with the text
    text_rect = text_surface.get_rect(topleft=(10, 50))  # Position the text at the mid right
    screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen
    return None

# Created by 5555194
def draw_restart() -> None:
    """
    Draws a restart message on the screen.

    This function creates a text surface with the message "Press R to restart", positions it at the middle of the screen, 
    and then blits this surface onto the screen.
    """
    font = pg.font.Font(None, 20)  # Create a font object
    text_surface = font.render(f"Press R to restart", True,
                               Color.WHITE.value)  # Create a surface with the text
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200))  # Position the text at the mid right
    screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen
    return None

# Created by 5590073
def draw_undo() -> None:
    """
    Draws an undo message on the screen.

    This function creates a text surface with the message "Press U to undo the last move", positions it at the middle of the screen, 
    and then blits this surface onto the screen.
    """
    font = pg.font.Font(None, 20)  # Create a font object
    text_surface = font.render(f"Press U to undo the last move", True,
                               Color.WHITE.value)  # Create a surface with the text
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 220))  # Position the text at the mid right
    screen.blit(text_surface, text_rect)  # Blit the text surface onto the screen
    return None


# Created by 5588113
class ListNode:
    """A class to represent a node in a linked list."""

    def __init__(self, data: int):
        """
        Initialize a node with the given data.

        Parameters:
            data (any): The data to be stored in the node.
        """
        self.data = data
        self.next = None


# Created by 5588113
class LinkedList:
    """A class to represent a linked list."""

    def __init__(self):
        """Initialize an empty linked list with a head node."""
        self.head = None
    
    def add(self, data: int) -> None:
        """
        Add a new node with the given data to the end of the linked list.

        Parameters:
            data (any): The data to be stored in the new node.
        """
        new_node = ListNode(data)
        if self.head is None:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
    
    def _partition(self, start: int, end: int, ascended: bool) -> int:
        """
        Partition the linked list segment around a quicksort pivot element.

        Parameters:
            start (Node): The start node of the segment to partition.
            end (Node): The end node of the segment to partition.
            ascended (bool): If True, sort in ascending order; otherwise, sort in descending order.

        Returns:
            Node: The pivot node after partitioning.
        """
        # Called by _quicksort
        pivot = start.data
        low = start
        high = start.next
        
        while high != end:
            if ascended:
                if high.data < pivot:
                    low = low.next
                    low.data, high.data = high.data, low.data
            else:
                if high.data > pivot:
                    low = low.next
                    low.data, high.data = high.data, low.data
            high = high.next
        
        low.data, start.data = start.data, low.data
        return low
    
    def _quicksort(self, start: int, end: int, ascended: bool) -> None:
        """
        Sort a linked list segment using the quick sort algorithm.

        Parameters:
            start (Node): The start node of the segment to sort.
            end (Node): The end node of the segment to sort.
            ascended (bool): If True, sort in ascending order; otherwise, sort in descending order.
        """
        # Called by sort()
        if start != end:
            pivot = self._partition(start, end, ascended)
            # Recursive call
            self._quicksort(start, pivot, ascended)
            self._quicksort(pivot.next, end, ascended)
    
    def sort(self, ascended: bool = True):
        """
        Sort the linked list in ascending or descending order using quick sort.

        Parameters:
            ascended (bool): If True, sort in ascending order; otherwise, sort in descending order.
        """
        if self.head is None:
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        self._quicksort(self.head, last_node.next, ascended)


# Created by 5590073 and 5588113, edited by 5555194
def draw_past_games_scores(past_games_scores: LinkedList, *args, **kwargs) -> None:
    """
    Draws the past game scores on the screen.

    This function sorts the scores in descending order and displays them at the top right corner of the screen.

    past_games_scores: A list of past game scores.
    """
    font = pg.font.Font(None, 15)  # Create a font object
    y_position = 40
    head_color = kwargs.get('head_color', Color.GREEN.value)  # Get the head color from kwargs
    
    # Apply quicksort the linked list
    past_games_scores.sort(ascended=False)

    # Draw the scores
    current_node = past_games_scores.head
    i = 1
    while current_node:
        score = current_node.data  # Retrieve the data from the node
        # Assign head color 
        if i == 1:
            color = head_color
        else:
            color = Color.WHITE.value
        text_surface = font.render(f"Best score {i}: {score}", True, color)  # Use the appropriate color
        text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH - 10, y_position))
        screen.blit(text_surface, text_rect)
        y_position += 10
        current_node = current_node.next
        i += 1


# Created by 5590073 and 5588113
def draw_past_games_times(past_games_times: LinkedList, *args, **kwargs) -> None:
    """
    Draws the past game times on the screen.

    This function sorts the times in ascending order and displays them at the top left corner of the screen.

    past_games_times: A list of past game times.
    """
    font = pg.font.Font(None, 15)  # Create a font object
    y_position = 80
    head_color = kwargs.get('head_color', Color.GREEN.value)  # Get the head color from kwargs
    
    # Apply quicksort the linked list
    past_games_times.sort(ascended=True)

    # Draw the times
    current_node = past_games_times.head
    i = 1
    while current_node:
        time = current_node.data  # Retrieve the data from the node
        # Assign head color 
        if i == 1:
            color = head_color
        else:
            color = Color.WHITE.value
        text_surface = font.render(f"Best time {i}: {time}", True, color)  # Use the appropriate color
        text_rect = text_surface.get_rect(topleft=(10, y_position))
        screen.blit(text_surface, text_rect)
        y_position += 10
        current_node = current_node.next
        i += 1


# Create a font object to render the welcome text on the screen

# Created by 5590073
font = pg.font.Font(None, 36)
font_surface = font.render("Welcome to the Snakes and Ladders", False, Color.WHITE.value)
clock = pg.time.Clock()

# Created by 5590073, edited by 5588113
def main():
    """Main game loop."""
    try:
        logging.info('Generating coordinates')
        # Initialize the board, player, progress bar, and timer
        board = Board(ROWS, COLUMNS)
        board.set_color(Color.WHITE.value)
        board.create_cells(generate_coordinates(board.rows, board.columns, CELL_SIZE_PIXELS))

        player = Player(position=PLAYER_START_POSITION)
        player.set_color(Color.PLAYER_COLOR.value)
        player.current_cell = board.cells_list[1]

        progress_bar = ProgressBar((10, 10), (200, 20))
        timer = Timer()
        
        # Asign games' scores and times as linked lists
        past_games_scores = LinkedList()
        past_games_times = LinkedList()

        # Generate snakes and ladders
        generator = Generator(board=board)
        generator.create_snakes_on_board(board=board)
        generator.create_ladders_on_board(board=board)

        # Create the adjacency list
        board.create_board_graph()
        # Calculate the shortest path
        shortest_path_length = board.calculate_shortest_path(start_cell_number=1, end_cell_number=ROWS*COLUMNS)
        
        # Created by 5590073
        running = True
        while running:
            # Handle events such as player movements, game reset and game quit
            running = handle_events(player, board, timer, past_games_scores, past_games_times)
            if running:
                draw_game_state(player,
                                board,
                                timer,
                                past_games_scores,
                                progress_bar,
                                player.moves,
                                past_games_times)
                update_game_state(player)

            # Update the display and set the frame rate to 60 FPS to ensure smooth gameplay
            pg.display.flip()
            clock.tick(60)
        # Quit the pygame module at the end
        logging.info('Quitting game')
        pg.quit()
        os._exit(0)
    except Exception as e:
        print(f"Error in game loop: {e}")
        pg.quit()
        os._exit(0)

# Created by 5590073, edited by 5555194 and 5588113
def handle_events(player, board, timer, past_games_scores, past_games_times):
    """
    Handles game events such as player movements, game reset, and game quit.

    player: The Player object representing the player.
    board: The Board object representing the game board.
    timer: The Timer object representing the game timer.
    past_games_scores: A list of scores from past games.
    past_games_times: A list of times from past games.
    return: False if the game is quit, True otherwise.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return False
        if event.type == pg.KEYDOWN:
            # If the key is the SPACE bar
            if event.key == pg.K_SPACE:
                logging.info('SPACE was pressed')
                # Change the player position based on the dice roll
                player.moves = roll_dice()
                current_cell_number = player.current_cell.number
                next_cell_number = current_cell_number + player.moves
                # Ensure that the player does not move beyond the last cell
                if next_cell_number <= 100:
                    player.position = change_position_to_cell(player, board.cells_list[next_cell_number])
                else:
                    player.position = change_position_to_cell(player, board.cells_list[100])
                    # Special bonus (if player doesn't encounter any snakes score is doubled)
                    if player.num_snakes == 0:
                        player.update_score(player.get_score())
                        # Increment the snake number so the score doesn't double if the player rolls the dice again at cell 100
                        player.snake_encountered()
                    # Simulate pressing the reset button to restart the game when the player reaches the last cell
                    pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_r))
            # Reset button
            if event.key == pg.K_r:
                logging.info('R was pressed')
                # Record the total score and time only if the player reaches the last cell
                if player.current_cell == board.cells_list[100]:
                    # Add data to linked lists
                    past_games_scores.add(player._score)
                    past_games_times.add(timer.get_elapsed_time())
                # Clear the board
                board.cells_list = {}
                board.snakes = []
                board.ladders = []
                # Recreate cells and entities
                board.create_cells(generate_coordinates(board.rows, board.columns, CELL_SIZE_PIXELS))
                # Regenerate snakes and ladders
                generator = Generator(board=board)
                generator.create_snakes_on_board(board=board)
                generator.create_ladders_on_board(board=board)
                # Recreate the adjacency list
                board.create_board_graph()
                # Recalculate the shortest path
                shortest_path_length = board.calculate_shortest_path(start_cell_number=1, end_cell_number=ROWS*COLUMNS)            
                # Reset player position, score, number of snakes encountered, timer, and number of steps made
                player.update_score((-1 * player._score) + 100)
                timer.reset()
                player.number_steps_made = 0
                player.position = change_position_to_cell(player, board.cells_list[1])
                player.reset_score()
                player.reset_num_snakes()
            # Undo button works when the player is not at the start cell (so the player can't undo the first move)
            if event.key == pg.K_u and player.current_cell != board.cells_list[1]:
                player.undo()
    return True


# Created by 5590073
def update_game_state(player):
    """
    Updates the game state based on the player's current cell.

    If the player's current cell contains an entity and the player is at the start of the entity, 
    the player reacts to the entity.

    player: The Player object representing the player.
    """
    if player.current_cell.contents is not None and player.current_cell == player.current_cell.contents.start_cell:
        try:
            player.react_to_entity(player.current_cell.contents)
        except Exception as e:
            print(f"Error reacting to entity: {e}")


# Created by 5590073, edited by 5555194
def draw_game_state(player, board, timer, past_games_scores, progress_bar, dice_value, past_games_times):
    """
    Draws the current game state on the screen.

    This includes the game board, player, timer, shortest distance, score, progress bar, past game scores, 
    past game times, dice value, and restart message.

    player: The Player object representing the player.
    board: The Board object representing the game board.
    timer: The Timer object representing the game timer.
    past_games_scores: A list of scores from past games.
    progress_bar: The ProgressBar object representing the game progress bar.
    dice_value: The current dice value.
    past_games_times: A list of times from past games.
    """
    try:
        # Each frame is filled with black color, so that the previous frame is not visible
        screen.fill((0, 0, 0))
        # Draw the board surface on the screen
        screen.blit(board.surface, (250, 150))
        board.update_cells()
        # Draw the player on the screen
        screen.blit(player.surface, player.rect)
        # Draw the font on the screen with the welcome message
        screen.blit(font_surface, (175, 50))
        # Draw the timer on the screen
        timer.draw()
        # Draw the shortest distance on the screen
        draw_shortest_distance(board.shortest_distance)
        # Draw the score on the screen
        draw_score(player.get_score())

        # Draw the test snakes and ladders
        for snake in board.snakes:
            snake.draw()

        for ladder in board.ladders:
            ladder.draw()

        # Update the progress bar
        progress = player.current_cell.number / len(board.cells_list)
        progress_bar.update(progress)
        # Draw the updated progress bar on the screen
        progress_bar.draw(screen)
        draw_past_games_scores(past_games_scores, head_color=Color.GREEN.value)
        draw_past_games_times(past_games_times, head_color=Color.GREEN.value)
        draw_number_steps_made(player)
        draw_dice_value(dice_value)
        draw_restart()
        draw_undo()
    except Exception as e:
        print(f"Error drawing game state: {e}")


if __name__ == "__main__":
    main()