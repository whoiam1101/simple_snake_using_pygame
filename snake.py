from random import randint
from math import floor
from enum import Enum
from pygame import Surface, Rect, Color
from pygame.draw import rect

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

def colorCalc(c1: Color, c2: Color, percent: int) -> Color:
    if percent > 1:
        percent = 2 - percent
    def f(v1: int, v2: int) -> int:
        return floor(v1 + (v2 - v1) * percent)
    r, g, b = f(c1.r, c2.r), f(c1.g, c2.g), f(c1.b, c2.b)
    return Color(r, g, b)

class MoveResult(Enum):
    OK = 0
    ATE_FOOD = 1
    HIT_TAIL = 2
    HIT_BORDER = 3

class Cell:

    def __init__(self, x: int, y: int, fromx: int = -1, fromy: int = -1) -> None:
        self.x = x
        self.y = y
        self.fromx = fromx
        self.fromy = fromy
        if fromy == -1:
            self.fromx = x
            self.fromy = y
        self.ishead = False
        self.progress = 0
    def tick(self, progress_step: int) -> None:
        self.progress += progress_step
        self.progress %= CELL_MAX_PROGRESS
    def coords(self, progress: int = 1) -> tuple[int, int]:
        x = (self.x - self.fromx) * progress + self.fromx
        y = (self.y - self.fromy) * progress + self.fromy
        return (x, y)
    def draw(self, progress: int, isdead: bool, screen: Surface, cell_size: int) -> None:
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
            main_color = colorCalc(HEAD_C1, HEAD_C2, percent)
            highlight_color = colorCalc(HEAD_H1, HEAD_H2, percent)
            shadow_color = colorCalc(HEAD_S1, HEAD_S2, percent)
        else:
            percent = self.progress / CELL_MAX_PROGRESS * 2
            main_color = colorCalc(SNAKE_C1, SNAKE_C2, percent)
            highlight_color = colorCalc(SNAKE_H1, SNAKE_H2, percent)
            shadow_color = colorCalc(SNAKE_S1, SNAKE_S2, percent)

        border = 2
        rect(screen, main_color, Rect(x, y, cell_size, cell_size))
        rect(screen, highlight_color, Rect(x, y, cell_size - border, border)) # top
        rect(screen, highlight_color, Rect(x, y, border, cell_size - border)) # left
        rect(screen, shadow_color, Rect(x + border, y + cell_size - border, cell_size - border, border)) # bottom
        rect(screen, shadow_color, Rect(x + cell_size - border, y, border, cell_size)) # right
    @classmethod
    def random(Cell, grid_width: int, grid_height: int):
        return Cell(randint(0, grid_width - 1), randint(0, grid_height - 1))

def nextCell(cell: Cell, next: Cell) -> None:
    cell.fromx = cell.x
    cell.fromy = cell.y
    cell.x = next.x
    cell.y = next.y

class Food:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y
        self.progress = 0
    def tick(self, progress_step: int) -> None:
        self.progress += progress_step
        self.progress %= FOOD_MAX_PROGRESS
    def iseaten(self, snake_cells: list[Cell]) -> bool:
        return any(self.equal(cell) for cell in snake_cells)
    def equal(self, cell: Cell) -> bool:
        return (cell.x, cell.y) == (self.x, self.y)
    def draw(self, progress: int, screen: Surface, cell_size: int) -> None:
        x, y = self.x * cell_size, self.y * cell_size

        percent = self.progress / FOOD_MAX_PROGRESS * 2
        main_color = colorCalc(FOOD_C1, FOOD_C2, percent)
        highlight_color = colorCalc(FOOD_H1, FOOD_H2, percent)
        shadow_color = colorCalc(FOOD_S1, FOOD_S2, percent)

        border = 2
        rect(screen, main_color, Rect(x, y, cell_size, cell_size))
        rect(screen, highlight_color, Rect(x, y, cell_size - border, border)) # top
        rect(screen, highlight_color, Rect(x, y, border, cell_size - border)) # left
        rect(screen, shadow_color, Rect(x + border, y + cell_size - border, cell_size - border, border)) # bottom
        rect(screen, shadow_color, Rect(x + cell_size - border, y, border, cell_size)) # right
    @classmethod
    def place(Food, grid_width: int, grid_height: int, exclude_cells: list[Cell]):
        while True:
            x = randint(0, grid_width - 1)
            y = randint(0, grid_height - 1)
            food = Food(x, y)
            if not food.iseaten(exclude_cells):
                return food

class Snake:
    def __iscolinear(self, dir1: tuple[int, int], dir2: tuple[int, int]) -> bool:
        """Checks if two direction vectors are collinear."""
        return dir1[0] * dir2[1] - dir1[1] * dir2[0] == 0
    def __init__(self, grid_width: int, grid_height: int, screen: Surface, cell_size: int) -> None:
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.screen = screen
        self.cell_size = cell_size
        self.reset()
    def reset(self) -> None:
        self.cells = [Cell.random(self.grid_width, self.grid_height)]
        self.cells[-1].ishead = True
        self.progress = 0
        self.dead_acc = 0
        self.score = 0
        self.food = Food.place(self.grid_width, self.grid_height, self.cells)
        self.direction = (0, 0)
        self.directions_queue = []
    def isdead(self) -> bool:
        return self.dead_acc > 0
    def push_direction(self, direction: tuple[int, int]) -> None:
        self.directions_queue.append(direction)
    def tick(self, progress_step: int) -> None:
        for cell in self.cells:
            cell.tick(progress_step)
        self.food.tick(progress_step)
        if self.dead_acc > 0:
            self.dead_acc -= progress_step
            if self.dead_acc <= 0:
                self.reset()
        else:
            self.progress += progress_step
            if self.progress >= 1:
                self.progress %= 1
                self.move()
    def _update_direction(self) -> None:
        """Updates the snake's direction from the directions queue."""
        while self.directions_queue and self.__iscolinear(self.direction, self.directions_queue[0]):
            self.directions_queue.pop(0)

        if self.directions_queue:
            self.direction = self.directions_queue.pop(0)

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
            for i in range(1, n -1):
                nextCell(self.cells[i], self.cells[i + 1])
            nextCell(self.cells[n-1], next_head)
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
            nextCell(self.cells[i], self.cells[i + 1])
        nextCell(self.cells[-1], next_head)
        self.cells[-1].ishead = True

    def move(self) -> MoveResult:
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
        self.food.draw(self.progress, self.screen, self.cell_size)
        for cell in self.cells:
            cell.draw(self.progress, self.isdead(), self.screen, self.cell_size)


        



