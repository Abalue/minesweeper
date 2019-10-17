from data.gui import *
from data.mineboard import Board
import sys  # need to rework state engine to remove sys.exit from menu


class Game:
    mine_img = pg.image.load('img/mine.png')
    ng_img = pg.image.load('img/ng_icon.png')
    rg_img = pg.image.load('img/rg_icon.png')

    def __init__(self):
        # Pygame components
        self.clock = pg.time.Clock()
        self.screen = None

        # state engine
        self.states = {'menu': self.new_board,
                       'reset': self.reset_board,
                       'game': self.play}
        self.next_state = 'menu'

        # game variables
        self.running = True
        self.click = None
        self.t = 0

        # game components
        self.board = None
        self.ng_button = None
        self.rg_button = None
        self.run()

    def new_board(self):
        """Creates a new board from menu settings"""
        size, mines = menu(self.clock)
        self.board = Board(tile_size=TILESIZE)
        self.board.create_new(size[0], size[1], mines)
        self.screen = pg.display.set_mode((self.board.image_width, self.board.image_height + self.board.tile_size))
        self.ng_button = Button((size[0]-0.8)*self.board.tile_size,
                                (size[1]+0.2)*self.board.tile_size,
                                self.board.tile_size*0.6, self.board.tile_size*0.6,
                                '', fill=True)
        self.rg_button = Button((size[0]-1.8)*self.board.tile_size,
                                (size[1]+0.2)*self.board.tile_size,
                                self.board.tile_size*0.6, self.board.tile_size*0.6,
                                '', fill=True)
        self.next_state = 'game'

    def reset_board(self):
        """Creates a new board based using current settings"""
        self.board.reset()
        self.next_state = 'game'

    def play(self):
        print('game')
        if not self.board.exploded and not self.board.solved:
            index = self.board.mouse_to_index((0, 0))
            if self.click == 'Left':
                self.board.reveal_tile(index[0], index[1])
            elif self.click == 'Right':
                self.board.place_flag(index[0], index[1])
            self.t += self.clock.get_time()
        if self.rg_button.update():
            self.next_state = 'reset'
        if self.ng_button.update():
            self.next_state = 'menu'

    def run(self):
        """Game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            self.clock.tick(FPS)

    def handle_events(self):
        """Gets user input (except mouse movement)"""
        self.click = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_n:
                    self.next_state = 'menu'
                if event.key == pg.K_r:
                    self.next_state = 'reset'
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = 'Left'
                if event.button == 3:
                    self.click = 'Right'

    def update(self):
        """Changes game state to next state"""
        self.states[self.next_state]()

    def draw(self):
        """Draw data board and data end messages"""
        self.screen.fill(pg.Color('white'))
        self.board.draw(self.screen)
        if self.board.solved:
            win_mess_1 = "Solved!"
            win_img_1 = BUTTONFONT.render(win_mess_1, True, FONTBLUE, BGGREY)
            self.screen.blit(win_img_1,
                             ((self.board.image_width - win_img_1.get_width())/2,
                              self.board.image_height/2 - int(0.5*TILESIZE)))
        self.ng_button.draw(self.screen)
        self.rg_button.draw(self.screen)
        self.screen.blit(Game.ng_img, self.ng_button.rect.topleft)
        self.screen.blit(Game.rg_img, self.rg_button.rect.topleft)

        time = int(min(self.t/1000, 9999))
        time_img = SCROLLFONT.render('Time: ' + str(time), False, FONTBLUE)
        self.screen.blit(time_img, (0.2 * self.board.tile_size, self.board.image_height + 0.2 * self.board.tile_size))

        flag_img = SCROLLFONT.render('Flags: ' + str(self.board.n_mines - self.board.n_flags), False, FONTBLUE)
        self.screen.blit(flag_img, (3 * TILESIZE, self.board.image_height + 0.2 * TILESIZE))

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
