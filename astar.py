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


    # now instead of just giving back the color, lets make spots change color

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

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

    def update_neighbors(self, grid): # neighbours of a square cannot be barriers/black (since barriers cannot be considered for the path)
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # For going DOWN checking if row position is a lower number than the total number of rows, and if the row below your square is a barrier
            self.neighbors.append(grid[self.row + 1][self.col]) # append that square to your list of neighbours.

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # For going UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # For going LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # for going RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])


    def __lt__(self, other): # lt stands for less than, we will use it to compare different spots to each other
        return False  # lets assume that the first spot is greater than the other spot

# manhattan/taxicab distance: the shortest L shaped path to reach from point A to point B

def h(p1, p2): # lets define the two points that will then be compared
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2) # abs meaning absolute number

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

# now lets make a list that holds all the data of the grid
def make_grid(rows, width):
    grid = []
    gagp = width // rows # width of entire grid // number of rows we have. decides the width of each of these cubes
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows) # pass in row, column, width, and total number of rows
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width): # this will draw the grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # horizontal lines drawn (win, color, x&y starting position, x&y ending position)
        for j in range(rows): # now lets flip the x and y values to get all the vertical lines
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

# now create a function that figures out the mouse position and which spot/square it is clicking on
def get_clicked_pos(pos, rows, width): # pos is the mouse position
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap 
    
    return row, col


def main(win, width): # win meaning window
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run: # if we press the x button at the top corner of the screen, the  pygame window is exited
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue # if the algorithm has started, make sure the user cannot change any obstacles other than quitting.

            if pygame.mouse.get_pressed()[0]: # if left mouse button pressed, do:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.make_start() # make this position the starting position (orange)

                elif not end and spot != start:
                    end = spot
                    end.make_end() # make this position the ending position (turquoise)

                elif spot != end and spot != start:
                    spot.make_barrier() # make this position a barrier (black)


            elif pygame.mouse.get_pressed()[1]:  #if middle mouse button pressed, do nothing:
                pass

            elif pygame.mouse.get_pressed()[2]: # if right mouse button pressed, do nothing:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            # now lets start writing the algorithm since the visualization tool is ready:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors()

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

    pygame.quit()

main(WIN, WIDTH)

    