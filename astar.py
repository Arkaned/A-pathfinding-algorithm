import pygame
import math
from queue import PriorityQueue #no need to import, should be already ijnstalled.

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0) # square already looked at
GREEN = (0, 255, 0) # square that is open to look at
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255) # square not yet looked at
BLACK = (0, 0, 0) # square that is a barrier
PURPLE = (128, 0, 128) # square that is part of the path
ORANGE = (255, 165, 0) # square that is the start node
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot: #spot aka nodes or cubes
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color  = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color == WHITE

    # now instead of just giving back the color, lets make spots change color

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win): # draw the color
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other): # lt stands for less than, we will use it to compare different spots to each other
        return False  # lets assume that the first spot is greater than the other spot

# manhattan/taxicab distance: the shortest L shaped path to reach from point A to point B

def h(p1, p2): # lets define the two points that will then be compared
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2) # abs meaning absolute number

# now lets make a list that holds all the data of the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid



    

    