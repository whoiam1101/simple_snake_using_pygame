from random import randint
from math import floor
from enum import Enum
from pygame import Surface, Rect, Color
from pygame.draw import rect

BORDER_COLOR = "black"

DEAD_COLOR = "red"

SNAKE_COLOR1 = Color(0, 255, 0)
SNAKE_COLOR2 = Color(0, 0, 255)
HEAD_COLOR1 = Color(105, 76, 2)
HEAD_COLOR2 = Color(77, 1, 8)

FOOD_COLOR1 = Color(255, 127, 0)
FOOD_COLOR2 = Color(255, 0, 255)

CELL_MAX_PROGRESS = 75
FOOD_MAX_PROGRESS = 30
BACKGROUND_MAX_PROGRESS = 20

def colorsGrid(width: int, height: int) -> list[list[tuple[Color, Color]]]:
    grid: list[list[tuple[Color, Color]]] = [[0 for j in range(0, height)] for i in range(0, width)]
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = randint(191, 215), randint(191, 215), randint(191, 215)
            r1 = r + randint(0, 40)
            g1 = g + randint(0, 40)
            b1 = b + randint(0, 40)
            r2 = r + randint(0, 40)
            g2 = g + randint(0, 40)
            b2 = b + randint(0, 40)
            grid[x][y] = (Color(r1, g1, b1), Color(r2, g2, b2))
    return grid

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
    def tick(self, percent: int) -> None:
        self.progress += percent
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
        rect(screen, BORDER_COLOR, Rect(x, y, cell_size, cell_size))
        if isdead:
            color = DEAD_COLOR
        elif self.ishead:
            color = colorCalc(HEAD_COLOR1, HEAD_COLOR2, self.progress / CELL_MAX_PROGRESS * 2)
        else:
            color = colorCalc(SNAKE_COLOR1, SNAKE_COLOR2, self.progress / CELL_MAX_PROGRESS * 2)
        rect(screen, color, Rect(x + 1, y + 1, cell_size - 2, cell_size - 2))
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
    def tick(self, percent: int) -> None:
        self.progress += percent
        self.progress %= FOOD_MAX_PROGRESS
    def iseaten(self, snake_cells: list[Cell]) -> bool:
        return any(self.equal(cell) for cell in snake_cells)
    def equal(self, cell: Cell) -> bool:
        return (cell.x, cell.y) == (self.x, self.y)
    def draw(self, progress: int, screen: Surface, cell_size: int) -> None:
        x, y = self.x * cell_size, self.y * cell_size
        rect(screen, BORDER_COLOR, Rect(x, y, cell_size, cell_size))
        color = colorCalc(FOOD_COLOR1, FOOD_COLOR2, self.progress / FOOD_MAX_PROGRESS * 2)
        rect(screen, color, Rect(x + 1, y + 1, cell_size - 2, cell_size - 2))
    @classmethod
    def place(Food, grid_width: int, grid_height: int, exclude_cells: list[Cell]):
        while True:
            x = randint(0, grid_width - 1)
            y = randint(0, grid_height - 1)
            food = Food(x, y)
            if not food.iseaten(exclude_cells):
                return food

class Snake:
    def __iscolinear(self, dir1: tuple[int, int], dir2: tuple[int, int]):
        return dir1 == dir2 or dir1[0] + dir2[0] == 0 and dir1[1] + dir2[1] == 0
    def __init__(self, grid_width: int, grid_height: int, screen: Surface, cell_size: int) -> None:
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.screen = screen
        self.cell_size = cell_size
        self.reset()
    def reset(self) -> None:
        self.cells = [Cell.random(self.grid_width, self.grid_height)]
        self.cells[0].ishead = True
        self.progress = 0
        self.dead_acc = 0
        self.score = 0
        self.background_acc = 0
        self.colors_grid = colorsGrid(self.grid_width, self.grid_height)
        self.food = Food.place(self.grid_width, self.grid_height, self.cells)
        self.direction = (0, 0)
        self.directions_queue = []
    def isdead(self) -> bool:
        return self.dead_acc > 0
    def push_direction(self, direction: tuple[int, int]) -> None:
        self.directions_queue.append(direction)
    def tick(self, percent: int) -> None:
        for cell in self.cells:
            cell.tick(percent)
        self.food.tick(percent)
        self.background_acc = (self.background_acc + percent) % BACKGROUND_MAX_PROGRESS
        if self.dead_acc > 0:
            self.dead_acc -= percent
            if self.dead_acc <= 0:
                self.reset()
        else:
            self.progress += percent
            if self.progress >= 1:
                self.progress %= 1
                self.move()
    def move(self) -> MoveResult:
        while len(self.directions_queue) > 0 and self.__iscolinear(self.direction, self.directions_queue[0]):
            self.directions_queue = self.directions_queue[1:]
        if len(self.directions_queue) > 0:
            self.direction = self.directions_queue[0]
            self.directions_queue = self.directions_queue[1:]
            
        n = len(self.cells)
        fx = self.cells[n - 1].x
        fy = self.cells[n - 1].y
        x = fx + self.direction[0]
        y = fy + self.direction[1]
        nexthead = Cell(x, y, fx, fy)
        if self.food.equal(nexthead):
            newCell = Cell(self.cells[0].x, self.cells[0].y, self.cells[0].fromx, self.cells[0].fromy)
            self.cells.insert(0, newCell)
            for i in range(1, n):
                nextCell(self.cells[i], self.cells[i + 1])
            nextCell(self.cells[n], nexthead)
            self.food = Food.place(self.grid_width, self.grid_height, self.cells)
            self.score += 1
            return MoveResult.ATE_FOOD
        if x < 0 or y < 0 or x >= self.grid_width or y >= self.grid_height:
            self.dead_acc = 10
            return MoveResult.HIT_BORDER
        hit_tail = False
        for i in range(1, n):
            if (x, y) == (self.cells[i].x, self.cells[i].y):
                hit_tail = True
        if hit_tail:
            self.dead_acc = 10
            return MoveResult.HIT_TAIL
        for i in range(0, n - 1):
            nextCell(self.cells[i], self.cells[i + 1])
        nextCell(self.cells[n - 1], nexthead)
        return MoveResult.OK
    def draw(self) -> None:
        for x in range(0, self.grid_width):
            for y in range(0, self.grid_height):
                dx = x * self.cell_size
                dy = y * self.cell_size
                color = colorCalc(self.colors_grid[x][y][0], self.colors_grid[x][y][1], self.background_acc / BACKGROUND_MAX_PROGRESS * 2)
                rect(self.screen, color, Rect(dx, dy, self.cell_size, self.cell_size))
        self.food.draw(self.progress, self.screen, self.cell_size)
        for cell in self.cells:
            cell.draw(self.progress, self.isdead(), self.screen, self.cell_size)


        



