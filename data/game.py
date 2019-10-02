from data.gui import *
from data.mineboard import MineBoard
import sys


class Game:
    mine_img = pg.image.load('img/mine.png')
    ng_img = pg.image.load('img/ng_icon.png')
    rg_img = pg.image.load('img/rg_icon.png')
    exp_img = pg.image.load('img/exploded.png')
    exp_img.set_colorkey(WHITE)

    def __init__(self):
        # pygame components
        self.clock = pg.time.Clock()
        self.screen = None

        # data settings
        self.running = True
        self.click = None

        # data components
        self.board = None
        self.ng_button = None
        self.rg_button = None
        self.new_board()

    def new_board(self):
        """Creates a new board from menu settings"""
        size, mines = menu(self.clock)
        self.board = MineBoard(mines, size)
        self.screen = pg.display.set_mode((TILESIZE * self.board.w, TILESIZE * (self.board.h + 1)))
        self.ng_button = Button((size[0]-0.8)*TILESIZE,
                                (size[1]+0.2)*TILESIZE,
                                TILESIZE*0.6, TILESIZE*0.6,
                                '', fill=True)
        self.rg_button = Button((size[0]-1.8)*TILESIZE,
                                (size[1]+0.2)*TILESIZE,
                                TILESIZE*0.6, TILESIZE*0.6,
                                '', fill=True)
        self.run()

    def reset_board(self):
        """Creates a new board based using current settings"""
        self.board = MineBoard(self.board.mines, (self.board.w, self.board.h))
        self.run()

    def run(self):
        """Game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(FPS)

    def handle_events(self):
        self.click = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_n:
                    self.new_board()
                if event.key == pg.K_r:
                    self.reset_board()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = 'Left'
                if event.button == 3:
                    self.click = 'Right'

    def update(self):
        """Update data board"""
        if not self.board.hit and not self.board.solved:
            self.board.update(self.click)
            self.board.t += self.clock.get_time()
            self.board.time = int(min(self.board.t/1000, 9999))
        if self.rg_button.update():
            self.reset_board()
        if self.ng_button.update():
            self.new_board()

    def draw(self):
        """Draw data board and data end messages"""
        self.screen.fill(pg.Color('white'))
        self.board.draw(self.screen)
        if self.board.solved:
            win_mess_1 = "Solved!"
            win_img_1 = BUTTONFONT.render(win_mess_1, True, FONTBLUE, BGGREY)
            self.screen.blit(win_img_1,
                             ((TILESIZE * self.board.w - win_img_1.get_width())/2,
                              TILESIZE * self.board.h/2 - int(0.5*TILESIZE)))
        self.ng_button.draw(self.screen)
        self.rg_button.draw(self.screen)
        self.screen.blit(Game.ng_img, self.ng_button.rect.topleft)
        self.screen.blit(Game.rg_img, self.rg_button.rect.topleft)
        pg.display.flip()


def menu(clock):
    """menu to select number of mines and board size"""
    running = True
    window_dimensions = 300, 400
    background_colour = pg.Color('lightgrey')
    display = pg.display.set_mode(window_dimensions)
    mine_img = pg.image.load('img/mine.png')
    pg.display.set_icon(mine_img)
    pg.display.set_caption('Minesweeper')

    # menu parts
    scroll_bar1 = Scrollbar(window_dimensions[0]*0.1, 50, window_dimensions[0]*0.8, 5, 80, 'Mines: ',
                            start_value=MINES)
    scroll_bar2 = Scrollbar(window_dimensions[0]*0.1, 100, window_dimensions[0]*0.8, 10, 40,
                            'Width: ', start_value=WIDTH)
    scroll_bar3 = Scrollbar(window_dimensions[0] * 0.1, 150, window_dimensions[0] * 0.8, 10, 20,
                            'Height: ', start_value=HEIGHT)
    start_button = Button(window_dimensions[0] * 0.3, 250, window_dimensions[0] * 0.4, 60, 'Start')

    # default data attributes
    size = HEIGHT, WIDTH
    n_of_mines = 5

    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    running = False
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        n_of_mines = scroll_bar1.update()
        w = scroll_bar2.update()
        h = scroll_bar3.update()
        started = start_button.update()
        if started:
            running = False
        size = w, h
        # draw
        display.fill(background_colour)
        scroll_bar1.draw(display)
        scroll_bar2.draw(display)
        scroll_bar3.draw(display)
        start_button.draw(display)
        pg.display.flip()

        clock.tick(FPS)

    return size, n_of_mines
