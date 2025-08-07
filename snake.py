"""
This module contains the Snake, Food, and Cell classes.
"""
from random import randint
from math import floor
from enum import Enum
from pygame import Surface, Rect, Color
from pygame.draw import rect
from collections.abc import Sequence

DEAD_COLOR = "red"

# Base colors
SNAKE_C1 = Color(34, 139, 34)   # forestgreen
SNAKE_C2 = Color(0, 100, 0)      # darkgreen
HEAD_C1 = Color(210, 105, 30)   # chocolate
HEAD_C2 = Color(139, 69, 19)    # saddlebrown
FOOD_C1 = Color(255, 69, 0)     # orangered
FOOD_C2 = Color(255, 140, 0)    # darkorange

# Highlight colors (lerped with white)
SNAKE_H1 = SNAKE_C1.lerp(Color('white'), 0.3)
SNAKE_H2 = SNAKE_C2.lerp(Color('white'), 0.3)
HEAD_H1 = HEAD_C1.lerp(Color('white'), 0.3)
HEAD_H2 = HEAD_C2.lerp(Color('white'), 0.3)
FOOD_H1 = FOOD_C1.lerp(Color('white'), 0.3)
FOOD_H2 = FOOD_C2.lerp(Color('white'), 0.3)

# Shadow colors (lerped with black)
SNAKE_S1 = SNAKE_C1.lerp(Color('black'), 0.4)
SNAKE_S2 = SNAKE_C2.lerp(Color('black'), 0.4)
HEAD_S1 = HEAD_C1.lerp(Color('black'), 0.4)
HEAD_S2 = HEAD_C2.lerp(Color('black'), 0.4)
FOOD_S1 = FOOD_C1.lerp(Color('black'), 0.4)
FOOD_S2 = FOOD_C2.lerp(Color('black'), 0.4)

CELL_MAX_PROGRESS = 75
FOOD_MAX_PROGRESS = 30

def color_calc(c1: Color, c2: Color, percent: float) -> Color:
    """
    Calculates a color between two colors based on a percentage.

    Args:
        c1: The first color.
        c2: The second color.
        percent: The percentage to interpolate by.

    Returns:
        The interpolated color.
    """
    if percent > 1:
        percent = 2 - percent
    def f(v1: int, v2: int) -> int:
        return floor(v1 + (v2 - v1) * percent)
    r, g, b = f(c1.r, c2.r), f(c1.g, c2.g), f(c1.b, c2.b)
    return Color(r, g, b)

class MoveResult(Enum):
    """The result of a snake's move."""
    OK = 0
    ATE_FOOD = 1
    HIT_TAIL = 2
    HIT_BORDER = 3

class Cell:
    """Represents a single cell of the snake."""
    __slots__ = ('x', 'y', 'fromx', 'fromy', 'ishead', 'progress')

    def __init__(self, x: int, y: int, fromx: int = -1, fromy: int = -1) -> None:
        """
        Initializes a Cell object.

        Args:
            x: The x-coordinate of the cell.
            y: The y-coordinate of the cell.
            fromx: The previous x-coordinate of the cell.
            fromy: The previous y-coordinate of the cell.
        """
        self.x = x
        self.y = y
        self.fromx = fromx
        self.fromy = fromy
        if fromy == -1:
            self.fromx = x
            self.fromy = y
        self.ishead = False
        self.progress = 0

    def tick(self, progress_step: float) -> None:
        """
        Updates the cell's progress.

        Args:
            progress_step: The amount to increment the progress by.
        """
        self.progress += progress_step
        self.progress %= CELL_MAX_PROGRESS

    def coords(self, progress: float = 1) -> tuple[float, float]:
        """
        Calculates the coordinates of the cell based on its progress.

        Args:
            progress: The progress of the cell's movement.

        Returns:
            A tuple containing the x and y coordinates.
        """
        x = (self.x - self.fromx) * progress + self.fromx
        y = (self.y - self.fromy) * progress + self.fromy
        return (x, y)

    def draw(self, progress: float, isdead: bool, screen: Surface, cell_size: int) -> None:
        """
        Draws the cell on the screen.

        Args:
            progress: The progress of the cell's movement.
            isdead: Whether the snake is dead.
            screen: The pygame surface to draw on.
            cell_size: The size of the cell.
        """
        if isdead:
            progress = 1
        x, y = self.coords(progress)
        x *= cell_size
        y *= cell_size

        if isdead:
            main_color = Color(DEAD_COLOR)
            highlight_color = main_color.lerp(Color('white'), 0.5)
            shadow_color = main_color.lerp(Color('black'), 0.5)
        elif self.ishead:
            percent = self.progress / CELL_MAX_PROGRESS * 2
            main_color = color_calc(HEAD_C1, HEAD_C2, percent)
            highlight_color = color_calc(HEAD_H1, HEAD_H2, percent)
            shadow_color = color_calc(HEAD_S1, HEAD_S2, percent)
        else:
            percent = self.progress / CELL_MAX_PROGRESS * 2
            main_color = color_calc(SNAKE_C1, SNAKE_C2, percent)
            highlight_color = color_calc(SNAKE_H1, SNAKE_H2, percent)
            shadow_color = color_calc(SNAKE_S1, SNAKE_S2, percent)

        border = 2
        rect(screen, main_color, Rect(x, y, cell_size, cell_size))
        rect(screen, highlight_color, Rect(x, y, cell_size - border, border)) # top
        rect(screen, highlight_color, Rect(x, y, border, cell_size - border)) # left
        rect(screen, shadow_color, Rect(x + border, y + cell_size - border, cell_size - border, border)) # bottom
        rect(screen, shadow_color, Rect(x + cell_size - border, y, border, cell_size)) # right

    @classmethod
    def random(cls, grid_width: int, grid_height: int) -> 'Cell':
        """
        Creates a new Cell at a random position.

        Args:
            grid_width: The width of the grid.
            grid_height: The height of the grid.

        Returns:
            A new Cell object.
        """
        return cls(randint(0, grid_width - 1), randint(0, grid_height - 1))

def next_cell(cell: Cell, next: Cell) -> None:
    """
    Updates a cell to the position of the next cell.

    Args:
        cell: The cell to update.
        next: The cell to move to.
    """
    cell.fromx = cell.x
    cell.fromy = cell.y
    cell.x = next.x
    cell.y = next.y

class Food:
    """Represents the food for the snake."""
    __slots__ = ('x', 'y', 'progress')

    def __init__(self, x: int = 0, y: int = 0) -> None:
        """
        Initializes a Food object.

        Args:
            x: The x-coordinate of the food.
            y: The y-coordinate of the food.
        """
        self.x = x
        self.y = y
        self.progress = 0

    def tick(self, progress_step: float) -> None:
        """
        Updates the food's progress.

        Args:
            progress_step: The amount to increment the progress by.
        """
        self.progress += progress_step
        self.progress %= FOOD_MAX_PROGRESS

    def is_eaten(self, snake_cells: Sequence[Cell]) -> bool:
        """
        Checks if the food has been eaten by the snake.

        Args:
            snake_cells: The cells of the snake.

        Returns:
            True if the food has been eaten, False otherwise.
        """
        return any(self.equal(cell) for cell in snake_cells)

    def equal(self, cell: Cell) -> bool:
        """
        Checks if the food is at the same position as a cell.

        Args:
            cell: The cell to compare with.

        Returns:
            True if the positions are the same, False otherwise.
        """
        return (cell.x, cell.y) == (self.x, self.y)

    def draw(self, progress: float, screen: Surface, cell_size: int) -> None:
        """
        Draws the food on the screen.

        Args:
            progress: The progress of the food's animation.
            screen: The pygame surface to draw on.
            cell_size: The size of the food.
        """
        x, y = self.x * cell_size, self.y * cell_size

        percent = self.progress / FOOD_MAX_PROGRESS * 2
        main_color = color_calc(FOOD_C1, FOOD_C2, percent)
        highlight_color = color_calc(FOOD_H1, FOOD_H2, percent)
        shadow_color = color_calc(FOOD_S1, FOOD_S2, percent)

        border = 2
        rect(screen, main_color, Rect(x, y, cell_size, cell_size))
        rect(screen, highlight_color, Rect(x, y, cell_size - border, border)) # top
        rect(screen, highlight_color, Rect(x, y, border, cell_size - border)) # left
        rect(screen, shadow_color, Rect(x + border, y + cell_size - border, cell_size - border, border)) # bottom
        rect(screen, shadow_color, Rect(x + cell_size - border, y, border, cell_size)) # right

    @classmethod
    def place(cls, grid_width: int, grid_height: int, exclude_cells: Sequence[Cell]) -> 'Food':
        """
        Places the food in a random position on the grid.

        Args:
            grid_width: The width of the grid.
            grid_height: The height of the grid.
            exclude_cells: A sequence of cells to exclude when placing the food.

        Returns:
            A new Food object.
        """
        while True:
            x = randint(0, grid_width - 1)
            y = randint(0, grid_height - 1)
            food = cls(x, y)
            if not food.is_eaten(exclude_cells):
                return food

class Snake:
    """Represents the snake."""
    __slots__ = (
        'grid_width', 'grid_height', 'screen', 'cell_size', 'cells', 'progress',
        'dead_acc', 'score', 'food', 'direction', 'directions_queue'
    )

    def __init__(self, grid_width: int, grid_height: int, screen: Surface, cell_size: int) -> None:
        """
        Initializes a Snake object.

        Args:
            grid_width: The width of the grid.
            grid_height: The height of the grid.
            screen: The pygame surface to draw on.
            cell_size: The size of the snake's cells.
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.screen = screen
        self.cell_size = cell_size
        self.reset()

    def reset(self) -> None:
        """Resets the snake to its initial state."""
        # Start snake in the center of the grid instead of random position
        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        self.cells: list[Cell] = [Cell(center_x, center_y)]
        self.cells[-1].ishead = True
        self.progress = 0.0
        self.dead_acc = 0.0
        self.score = 0
        self.food = Food.place(self.grid_width, self.grid_height, self.cells)
        self.direction = (1, 0)  # Start moving right
        self.directions_queue: list[tuple[int, int]] = []
    
    def save_score_and_reset(self) -> None:
        """Saves the current score to high scores and resets the snake."""
        from high_scores import add_score
        if self.score > 0:  # Only save non-zero scores
            add_score(self.score)
        self.reset()

    def is_dead(self) -> bool:
        """
        Checks if the snake is dead.

        Returns:
            True if the snake is dead, False otherwise.
        """
        return self.dead_acc > 0

    def push_direction(self, direction: tuple[int, int]) -> None:
        """
        Adds a direction to the queue.

        Args:
            direction: The direction to add.
        """
        self.directions_queue.append(direction)

    def tick(self, progress_step: float) -> None:
        """
        Updates the snake's state.

        Args:
            progress_step: The amount to increment the progress by.
        """
        for cell in self.cells:
            cell.tick(progress_step)
        self.food.tick(progress_step)
        if self.dead_acc > 0:
            self.dead_acc -= progress_step
            if self.dead_acc <= 0:
                self.save_score_and_reset()
        else:
            self.progress += progress_step
            if self.progress >= 1:
                self.progress %= 1
                self.move()

    def _update_direction(self) -> None:
        """Updates the snake's direction from the directions queue."""
        while self.directions_queue and self.__is_colinear(self.direction, self.directions_queue[0]):
            self.directions_queue.pop(0)

        if self.directions_queue:
            self.direction = self.directions_queue.pop(0)

    def __is_colinear(self, dir1: tuple[int, int], dir2: tuple[int, int]) -> bool:
        """Checks if two direction vectors are collinear."""
        return dir1[0] * dir2[1] - dir1[1] * dir2[0] == 0

    def _get_next_head(self) -> Cell:
        """Calculates the position of the next head cell."""
        head = self.cells[-1]
        return Cell(head.x + self.direction[0], head.y + self.direction[1], head.x, head.y)

    def _handle_food_collision(self, next_head: Cell) -> bool:
        """Checks for and handles food collisions."""
        if self.food.equal(next_head):
            self.cells[-1].ishead = False
            new_cell = Cell(self.cells[0].x, self.cells[0].y, self.cells[0].fromx, self.cells[0].fromy)
            self.cells.insert(0, new_cell)
            n = len(self.cells)
            for i in range(1, n - 1):
                next_cell(self.cells[i], self.cells[i + 1])
            next_cell(self.cells[n-1], next_head)
            self.cells[-1].ishead = True
            self.food = Food.place(self.grid_width, self.grid_height, self.cells)
            self.score += 1
            return True
        return False

    def _check_wall_collision(self, next_head: Cell) -> bool:
        """Checks for wall collisions."""
        return next_head.x < 0 or next_head.y < 0 or next_head.x >= self.grid_width or next_head.y >= self.grid_height

    def _check_tail_collision(self, next_head: Cell) -> bool:
        """Checks for tail collisions."""
        return any((next_head.x, next_head.y) == (cell.x, cell.y) for cell in self.cells[1:])

    def _move_body(self, next_head: Cell) -> None:
        """Moves the snake's body forward."""
        self.cells[-1].ishead = False
        for i in range(len(self.cells) - 1):
            next_cell(self.cells[i], self.cells[i + 1])
        next_cell(self.cells[-1], next_head)
        self.cells[-1].ishead = True

    def move(self) -> MoveResult:
        """
        Moves the snake one step forward.

        Returns:
            The result of the move.
        """
        self._update_direction()

        next_head = self._get_next_head()

        if self._handle_food_collision(next_head):
            return MoveResult.ATE_FOOD

        if self._check_wall_collision(next_head):
            self.dead_acc = 10
            return MoveResult.HIT_BORDER

        if self._check_tail_collision(next_head):
            self.dead_acc = 10
            return MoveResult.HIT_TAIL

        self._move_body(next_head)
        return MoveResult.OK

    def draw(self) -> None:
        """Draws the snake and food on the screen."""
        self.food.draw(self.progress, self.screen, self.cell_size)
        for cell in self.cells:
            cell.draw(self.progress, self.is_dead(), self.screen, self.cell_size)
