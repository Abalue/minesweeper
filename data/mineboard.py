from settings import *
from random import randint as rand


class MineBoard:
    font = pg.font.Font(None, TILESIZE)
    mine_img = pg.image.load('img/mine.png')
    flag_img = pg.image.load('img/flag.png')
    tile_img = pg.image.load('img/tile.png')
    bad_mine_img = pg.image.load('img/bad_mine.png')

    neighbours = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
    colours = {1: 'blue', 2: 'darkgreen', 3: 'red', 4: 'purple', 5: ' maroon', 6: 'turquoise', 7: 'black', 8: 'gray'}

    def __init__(self, mines, size):
        self.board = None
        self.top_board = None
        self.w = size[0]
        self.h = size[1]
        self.mines = mines
        self.reset_board()
        self.t = 0
        self.time = 0

    @property
    def solved(self):
        if not self.hit:
            return self.w * self.h - sum(row.count(1) for row in self.top_board) == self.mines

    @property
    def flags_left(self):
        return self.mines - sum(row.count('f') for row in self.top_board)

    @property
    def hit(self):
        return any('hm' in row for row in self.board)

    def reset_board(self):
        """Creates a new board"""
        # board is a list of a list i.e. board[y][x]
        # board consists of 0-8: number of surrounding mines, 'm': mine, 'hm': hit mine, 'bm' revealed mine under flag
        self.board = self.blank_board()
        self.top_board = self.blank_board()

        # place mines
        current_mines = 0
        while current_mines < self.mines:
            row = rand(0, self.h-1)
            col = rand(0, self.w-1)
            if self.board[row][col] == 0:
                self.board[row][col] = 'm'
                current_mines += 1

        # count neighbours
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                # get list of indexes for all neighbour cells
                neighbours = [self.board[i + n[0]][j + n[1]] for n in MineBoard.neighbours if
                              self.inside(i + n[0], j + n[1])]
                # if cell not a mine count number of mines in neighbour cells
                if not col:
                    self.board[i][j] = neighbours.count('m')

    def blank_board(self):
        return [[0] * self.w for _ in range(self.h)]

    def update(self, click):
        index = self.mouse_to_index()
        if click == 'Left':
            self.reveal(index)
        elif click == 'Right':
            self.place_flag(index)

        # reveal mines and missed flags
        if self.hit:
            for i, row in enumerate(self.board):
                for j, col in enumerate(row):
                    # if mine not flagged, reveal
                    if col == 'm' and self.top_board[i][j] != 'f':
                        self.top_board[i][j] = 1
                    elif col != 'm' and self.top_board[i][j] == 'f':
                        self.board[i][j] = 'bm'
                        self.top_board[i][j] = 1

    def reveal(self, index):
        i, j = index
        # if index inside board and yet to be revealed/not flagged
        if self.inside(i, j) and not self.top_board[i][j]:
            # reveal cell
            self.top_board[i][j] = 1
            # if cell revealed is mine, set it to hit
            if self.board[i][j] == 'm':
                self.board[i][j] = 'hm'
            # if no surrounding mines iterate through neighbours
            elif self.board[i][j] == 0:
                for n_i, n_j in [[i + n[0], j + n[1]] for n in MineBoard.neighbours if
                                 self.inside(i + n[0], j + n[1])]:
                    # if unrevealed
                    if not self.top_board[n_i][n_j]:
                        self.reveal((n_i, n_j))

    def place_flag(self, index):
        i, j = index
        # if inside board and not revealed
        if self.inside(i, j) and self.top_board[i][j] != 1:
            if self.top_board[i][j] != 'f':
                self.top_board[i][j] = 'f'
            else:
                self.top_board[i][j] = 0

    def inside(self, i, j):
        return 0 <= j < self.w and 0 <= i < self.h

    @ staticmethod
    def mouse_to_index():
        mouse_pos = pg.mouse.get_pos()
        return int(mouse_pos[1]/TILESIZE), int(mouse_pos[0]/TILESIZE)

    def draw_grid(self, surface):
        for x in range(self.w):
            pg.draw.line(surface, pg.Color('black'), ((x+1) * TILESIZE, 0),
                         ((x+1) * TILESIZE, surface.get_height() - TILESIZE))
        for y in range(self.h):
            pg.draw.line(surface, pg.Color('black'), (0, (y+1) * TILESIZE),
                         (surface.get_width(), (y+1) * TILESIZE))

    def draw_bottom_board(self, surface):
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                # draw mines
                if col == 'm':
                    surface.blit(MineBoard.mine_img, (x * TILESIZE, y * TILESIZE))
                # draw number of neighbours
                if col in MineBoard.colours:
                    num_img = MineBoard.font.render(str(col),
                                                    False, pg.Color(MineBoard.colours[col]))
                    surface.blit(num_img, (x * TILESIZE + 0.35 * TILESIZE, y * TILESIZE + 0.2 * TILESIZE))
                # draw hit mine
                if col == 'hm':
                    pg.draw.rect(surface, RED, (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE))
                    surface.blit(MineBoard.mine_img, (x * TILESIZE, y * TILESIZE))
                # draw missed flags
                if col == 'bm':
                    surface.blit(MineBoard.bad_mine_img, (x * TILESIZE, y * TILESIZE))

    def draw_top_board(self, surface):
        for y, row in enumerate(self.top_board):
            for x, col in enumerate(row):
                if col == 0:
                    surface.blit(MineBoard.tile_img, (x * TILESIZE, y * TILESIZE))
                if col == 'f':
                    surface.blit(MineBoard.tile_img, (x * TILESIZE, y * TILESIZE))
                    surface.blit(MineBoard.flag_img, (x * TILESIZE, y * TILESIZE))

    def draw_time(self, surface):
        time_cor = min(self.time, 9999)
        time_img = SCROLLFONT.render('Time: ' + str(time_cor), False, FONTBLUE)
        surface.blit(time_img, (0.2*TILESIZE, self.h*TILESIZE + 0.2 * TILESIZE))

    def draw_flags(self, surface):
        """Draws number of mines remaining based on flags placed"""
        flag_img = SCROLLFONT.render('Flags: ' + str(self.flags_left), False, FONTBLUE)
        surface.blit(flag_img, (3*TILESIZE, self.h*TILESIZE + 0.2*TILESIZE))

    def draw(self, surface):
        self.draw_bottom_board(surface)
        self.draw_top_board(surface)
        self.draw_grid(surface)

        # draw gui
        self.draw_time(surface)
        self.draw_flags(surface)
