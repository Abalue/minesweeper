from settings import *


class Scrollbar:
    def __init__(self, x, y, width, min_value, max_value, message, start_value=0):
        self.message = message

        # set values
        self.min_value = min_value
        self.max_value = max_value
        self.value = start_value
        if not min_value <= start_value <= max_value:
            self.value = min_value

        # set rects
        self.box_rect = pg.Rect(x, y, width, 20)
        self.scroll_rect = pg.Rect(x+1, y+1, int(width/8), self.box_rect.height-2)
        self.scroll_rect = pg.Rect(self.value_to_pos(), y + 1, int(width / 8), self.box_rect.height - 2)

        # set hold parameters
        self.hold_diff = 0
        self.hold_time = 50

        self.hovering = False
        self.mouse_last_pressed = False
        self.holding = False

    def value_to_pos(self):
        return self.box_rect.x + 1 + (self.value - self.min_value) / (self.max_value - self.min_value) * (
                    self.box_rect.width - self.scroll_rect.width - 2)

    def pos_to_value(self):
        return self.min_value + (self.max_value - self.min_value) * (self.scroll_rect.x - self.box_rect.x - 1) / (
                    self.box_rect.width - self.scroll_rect.width - 2)

    def update(self):
        """Update scroll bar depending on mouse"""
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()[0]
        if self.scroll_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.hovering = True
            if mouse_pressed:
                if not self.holding and not self.mouse_last_pressed:
                    self.hold_diff = mouse_pos[0]-self.scroll_rect.x
                    self.holding = True
        else:
            if self.box_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                if mouse_pressed:
                    # if clicking in scroll box but not on scroller move towards mouse
                    if not self.holding and not self.mouse_last_pressed:
                        if mouse_pos[0] > self.scroll_rect.midtop[0]:
                            self.scroll_rect.x = min(self.scroll_rect.x + self.box_rect.width / 8,
                                                     mouse_pos[0] - self.scroll_rect.width / 2,
                                                     self.box_rect.x + self.box_rect.width - self.scroll_rect.width - 1)
                        if mouse_pos[0] < self.scroll_rect.midtop[0]:
                            self.scroll_rect.x = max(self.scroll_rect.x - self.box_rect.width / 8,
                                                     mouse_pos[0] - self.scroll_rect.width / 2,
                                                     self.box_rect.x + 1)
            if not self.holding:
                self.hovering = False
        if not mouse_pressed:
            self.mouse_last_pressed = False
            self.holding = False
        else:
            self.mouse_last_pressed = True
            if self.holding:
                self.scroll_rect.x = max(min(self.box_rect.right-self.scroll_rect.width-1,
                                             mouse_pos[0]-self.hold_diff), self.box_rect.x+1)

        self.value = round(self.pos_to_value())
        return self.value

    def draw(self, surface):
        value_img = SCROLLFONT.render(self.message + str(int(self.value)), False, FONTBLUE)
        # draw bounding box
        pg.draw.rect(surface, pg.Color('white'), self.box_rect)
        pg.draw.rect(surface, pg.Color('black'), self.box_rect, 1)
        if self.hovering:
            pg.draw.rect(surface, FONTBLUE, self.scroll_rect)
        else:
            pg.draw.rect(surface, pg.Color('gray'), self.scroll_rect)
        surface.blit(value_img, (self.box_rect.x+5, self.box_rect.top - self.box_rect.height))


class Button:
    def __init__(self, x, y, width, height, message, fill=False):
        self.rect = pg.Rect(x, y, width, height)
        self.fill = fill
        self.message = message
        self.hovering = False
        self.mouse_last_pressed = False

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.hovering = True
            if mouse_pressed and not self.mouse_last_pressed:
                return True
        else:
            self.hovering = False
        if mouse_pressed:
            self.mouse_last_pressed = True
        else:
            self.mouse_last_pressed = False

        return False

    def draw(self, surface):
        mess_img = BUTTONFONT.render(self.message, False, FONTBLUE)
        bg_col = WHITE
        if self.hovering:
            mess_img = BUTTONFONT.render(self.message, False, FONTBLUE.correct_gamma(0.5))
            if self.fill:
                bg_col = FONTBLUE
        pg.draw.rect(surface, bg_col, self.rect)
        pg.draw.rect(surface, BLACK, self.rect, 1)
        surface.blit(mess_img, (self.rect.x+self.rect.width/2-mess_img.get_width()/2,
                                self.rect.y+self.rect.height/2-mess_img.get_height()/2))
