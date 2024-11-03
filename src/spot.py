import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.neighbours = []
        self.color = WHITE

    def get_pos(self):
        return (self.row, self.col)
    
    def is_closed(self):
        return self.color == RED
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def is_barrier(self):
         return self.color == BLACK
    
    def make_open(self):
        self.color = GREEN
    
    def make_closed(self):
        self.color = RED

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbours(self, grid ):
        self.neighbours = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # NORTH
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # WEST
            self.neighbours.append(grid[self.row][self.col - 1])
        
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # SOUTH
            self.neighbours.append(grid[self.row + 1][self.col])
        
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # EAST
            self.neighbours.append(grid[self.row][self.col + 1])