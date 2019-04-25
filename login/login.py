import curses

class Window:
    def __init__(self, options, height=0, width=0):
        self.options = options
        self.height = height
        self.width = width

    def init_screen(self, stdscr):
        stdscr.clear()
        stdscr.refresh()

        min_h, min_w = 50, 100
        term_height, term_width = stdscr.getmaxyx()

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
        return (abs(center)+center)//2 # Turning negative numbers to 0


    def draw_options(self, stdscr, separation=5):
        start_y_choices = self.height//2
        y_step = range(0, len(self.options) * separation, separation)
        option_nums = range(1, len(self.options) + 1)

        for step, option, num in zip(y_step, self.options, option_nums):
            x_val = self._center_width(option)
            stdscr.addstr(start_y_choices + step, x_val, f'{num}: {option}')


class Login(Window):
    def __init__(self):
        pass


class CreateAcc(Window):
    def __init__(self):
        pass



test = Window(['Login', 'Create an Account'])
curses.wrapper(test.draw_options)