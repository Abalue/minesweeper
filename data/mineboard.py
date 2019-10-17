import pygame as pg
from random import randint as rand
from math import floor


class Board:
    """Stores minesweeper information and handles interaction such as placing a flag or revealing a tile (input is
     handled separately)"""
    neighbours = [[-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]
    colours = {1: 'blue', 2: 'darkgreen', 3: 'red', 4: 'purple', 5: ' maroon', 6: 'turquoise', 7: 'black', 8: 'gray'}
    difficulties = {'easy': [10, 10, 10], 'intermediate': [40, 16, 16], 'expert': [99, 30, 16]}

    def __init__(self, difficulty='easy', tile_size=32):
        """Boards are created in the create_new() function. Many variables are stored as a property as they can be
        calculated from the top_board and bottom_board variables"""
        self.top = None
        self.bottom = None

        settings = Board.difficulties[difficulty]
        self.create_new(settings[1], settings[2], settings[0])

        self.tile_size = tile_size

        self.font = pg.font.SysFont('', tile_size)
        self.mine_img = pg.transform.scale(pg.image.load('img/mine.png'), (self.tile_size, self.tile_size))
        self.tile_img = pg.transform.scale(pg.image.load('img/tile.png'), (self.tile_size, self.tile_size))
        self.bad_mine_img = pg.transform.scale(pg.image.load('img/bad_mine.png'), (self.tile_size, self.tile_size))
        self.flag_img = pg.transform.scale(pg.image.load('img/flag.png'), (self.tile_size, self.tile_size))

    def create_new(self, width, height, mines):
        """Creates a new top board and bottom board and places mines in random locations"""
        # create empty boards
        self.top = [[0] * width for _ in range(height)]
        self.bottom = [[0] * width for _ in range(height)]

        # place mines
        mines_placed = 0
        while mines_placed < mines:
            i, j = rand(0, height-1), rand(0, width-1)
            if not self.bottom[i][j]:
                self.bottom[i][j] = -1
                mines_placed += 1

        # count adjacent mines
        for i in range(height):
            for j in range(width):
                if self.bottom[i][j] != -1:
                    self.bottom[i][j] = sum(  # sum of adjacent mines from list of booleans that is created
                        [self.bottom[i + neighbour[0]][j + neighbour[1]] == -1 for neighbour in Board.neighbours if
                         self.index_in_board(i + neighbour[0], j + neighbour[1])])  # if inside of board

    def reset(self):
        """Creates a new board using the current boards settings"""
        self.create_new(self.width, self.height, self.n_mines)

    @property
    def width(self):
        """Returns width of current board"""
        return len(self.bottom[0])

    @property
    def image_width(self):
        return self.width*self.tile_size

    @property
    def image_height(self):
        return self.height*self.tile_size

    @property
    def height(self):
        """Returns length of current board"""
        return len(self.bottom)

    @property
    def n_mines(self):
        """The number of mines in current board"""
        return sum([row.count(-1) + row.count(-2) for row in self.bottom])

    @property
    def n_flags(self):
        """The number of flags placed in current board"""
        return sum([row.count(2) for row in self.top])

    @property
    def exploded(self):
        """Have any of the mines have been revealed"""
        return any(-2 in row for row in self.bottom)

    @property
    def solved(self):
        """Is the number of unrevealed tiles equal to the number of mines"""
        return self.n_mines == self.width*self.height - sum([row.count(1) for row in self.top])

    def reveal_tile(self, i, j):
        """Reveals tile using index and if there is no adjacent mines will clear all adjacent tiles"""
        if self.index_in_board(i, j):
            if self.top[i][j] != 2:  # reveal unless flag is placed
                self.top[i][j] = 1
                if self.bottom[i][j] == -1:  # if revealed is mine set mine to hit and reveal board
                    self.bottom[i][j] = -2
                    self.reveal_board()
                elif not self.bottom[i][j]:  # if revealed empty reveal all neighbours
                    for neighbour in [item for item in self.neighbours if self.index_in_board(i+item[0], j+item[1])]:
                        if not self.top[i+neighbour[0]][j+neighbour[1]]:
                            self.reveal_tile(i+neighbour[0], j + neighbour[1])

    def place_flag(self, i, j):
        """Places a flag on top board"""
        if self.index_in_board(i, j):
            if self.top[i][j] != 1:  # change flag if not revealed
                self.top[i][j] = 2 - self.top[i][j]

    def reveal_board(self):
        """Will reveal entire board except on flags that are on mines. Flags not on mines will become bad mines"""
        for i, row in enumerate(self.top):
            for j, item in enumerate(row):
                if not (item == 2 and self.bottom[i][j] == -1):  # reveal unless mine is flagged
                    self.top[i][j] = 1
                    if item == 2:  # if incorrectly flagged set as bad mine
                        self.bottom[i][j] = -3

    def index_in_board(self, i, j):
        """Checks if index is within the limits of the board"""
        return 0 <= i < self.height and 0 <= j < self.width

    def mouse_to_index(self, offset):
        """Converts mouse position to coordinate on board. Offset is the (x, y) distance from board to display"""
        # NEED TO IMPLEMENT A FEATURE THAT WILL ADD ON ANY PIXELS IF BOARD IS NOT AT THE TOP LEFT OF SCREEN
        mouse_pos = pg.mouse.get_pos()
        return floor((mouse_pos[1] - offset[1]) / self.tile_size), floor((mouse_pos[0] - offset[0]) / self.tile_size)

    def draw(self, display):
        """Renders the board using Pygame to the selected display"""
        for i, row in enumerate(self.bottom):
            for j, bot in enumerate(row):
                # DRAW BOTTOM BOARD
                # Draws adjacent mine numbers
                if bot in Board.colours:
                    display.blit(self.font.render(str(bot), True, pg.Color(Board.colours[bot])),  # number image
                                 ((j + 0.35) * self.tile_size, (i + 0.2) * self.tile_size))  # number location
                # Draw mines
                if bot == -1:
                    display.blit(self.mine_img, (j*self.tile_size, i*self.tile_size))
                # Draw hit mines
                if bot == -2:
                    pg.draw.rect(display,
                                 pg.Color('red'),
                                 (j*self.tile_size, i*self.tile_size, self.tile_size, self.tile_size))
                    display.blit(self.mine_img, (j*self.tile_size, i*self.tile_size))
                # Draw bad mines
                if bot == -3:
                    display.blit(self.bad_mine_img, (j*self.tile_size, i*self.tile_size))

                # DRAW TOP BOARD AND GRID
                top = self.top[i][j]
                if top != 1:
                    display.blit(self.tile_img, (j*self.tile_size, i*self.tile_size))
                if top == 2:
                    display.blit(self.flag_img, (j*self.tile_size, i*self.tile_size))
                # Draw grid
                if i > 0:
                    pg.draw.line(display,
                                 pg.Color('black'),
                                 (0, i*self.tile_size),
                                 (self.width*self.tile_size, i*self.tile_size),
                                 1)
                if j > 0:
                    pg.draw.line(display,
                                 pg.Color('black'),
                                 (j*self.tile_size, 0),
                                 (j*self.tile_size, self.height*self.tile_size))
