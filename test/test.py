import curses


class Page:

    def __init__(self, stdscr):
        self.stdscr = stdscr

    def _init_screen(self):
        self.stdscr.clear()
        self.stdscr.refresh()

        min_h, min_w = 50, 100
        term_height, term_width = self.stdscr.getmaxyx()

        if term_height < min_h:
            curses.resize_term(min_h, term_width)
            term_height = min_h
        if term_width < min_w:
            curses.resize_term(term_height, min_w)
            term_width = min_w

        self.height, self.width = term_height, term_width

    def _center_width(self, text):
        line_len = len(text.split('\n')[0])
        center = self.width // 2 - line_len // 2
        return (abs(center)+center) // 2  # Turning negative numbers to 0

    def draw_short_answer(self, question):
        self._init_screen()
        start_x = self._center_width(question)
        start_y = self.height // 4
        self.stdscr.addstr(start_y, start_x, question)
        self.stdscr.refresh()
        self.stdscr.getch()

    def draw_multiple_choice(self, question, answers):
        pass


def main(stdscr):
    page = Page(stdscr)
    page.draw_short_answer('Question?')


curses.wrapper(main)
