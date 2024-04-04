import random as rd

class Entity:
    """
    Represents an entity on a board dictionary, which corresponds to a cell number for teleportation.
    """

    def __init__(self, board_dictionary, columns=10, rows=10):
        """
        Initialize Entity with the provided board dictionary, columns, and rows.
        """
        self.board = board_dictionary
        self.end_position = columns * rows
        self.entity_number = rows // 2

    def generate(self):
        """
        Generate entities on the board.
        """
        pass

class Ladders(Entity):
    """
    Represents ladders on the board, where the entity_end is always more than entity_start.
    Implements hierarchical inheritance by inheriting from the Entity class.
    """

    def __init__(self, board_dictionary, columns=10, rows=10):
        """
        Initialize Ladders with the provided board dictionary, columns, and rows.
        """
        super().__init__(board_dictionary, columns, rows)

    def generate(self):
        """
        Generate ladders on the board.
        """
        # Generate a limited number of entities (half of the row numbers)
        for _ in range(self.entity_number + 1):
            # Generate two random board positions ensuring end is more than start
            entity_start = rd.randint(2, self.end_position)
            entity_end = rd.randint(entity_start + 1, self.end_position)
            
            # Ensure the generated ladder does not overlap with existing entities
            while self.board[entity_start] != 0 or self.board[entity_end] != 0:
                entity_end = rd.randint(entity_start + 1, self.end_position)
            
            # Place the ladder on the board
            self.board[entity_start] = entity_end

        return self.board

class Snakes(Entity):
    """
    Represents snakes on the board, where the entity_start is always more than entity_end.
    Implements hierarchical inheritance by inheriting from the Entity class.
    """

    def __init__(self, board_dictionary, columns=10, rows=10):
        """
        Initialize Snakes with the provided board dictionary, columns, and rows.
        """
        super().__init__(board_dictionary, columns, rows)

    def generate(self):
        """
        Generate snakes on the board.
        """
        # Generate a limited number of entities (half of the row numbers)
        for _ in range(self.entity_number + 1):
            # Generate two random board positions ensuring start is more than end
            entity_start = rd.randint(2, self.end_position)
            entity_end = rd.randint(2, entity_start - 1)
            
            # Ensure the generated snake does not overlap with existing entities
            while self.board[entity_start] != 0 or self.board[entity_end] != 0:
                entity_end = rd.randint(2, entity_start - 1)
            
            # Place the snake on the board
            self.board[entity_start] = entity_end

        return self.board

# Initialize a plain board with all values set to 0
plain_board = {i: 0 for i in range(1, 101)}

# Create an instance of Ladders and generate ladders on the board
ladders = Ladders(plain_board)
modified_board = ladders.generate()

# Create an instance of Snakes and generate snakes on the board
snakes = Snakes(modified_board)
modified_board = snakes.generate()

print(modified_board)
