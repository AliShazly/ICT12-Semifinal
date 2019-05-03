import os
import curses
import binascii
import hashlib


def hash_salt(pwd):
    random_bytes = os.urandom(8)
    salt = binascii.hexlify(random_bytes).decode('ascii')
    hash_bytes = hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), salt.encode('utf-8'), 100000)
    hashed_pwd = binascii.hexlify(hash_bytes)
    return hashed_pwd, salt


class Window:
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
        return (abs(center) + center) // 2 # Turning negative numbers to 0


    def draw_options(self, options, separation=5):
        self._init_screen()
        start_y_choices = self.height//2
        y_step = range(0, len(options) * separation, separation)
        option_nums = range(1, len(options) + 1)

        for step, option, num in zip(y_step, options, option_nums):
            x_val = self._center_width(option)
            self.stdscr.addstr(start_y_choices + step, x_val, f'{num}: {option}')
        while True:
            choice = chr(self.stdscr.getch())
            if choice in (str(i) for i in range(1, len(options) + 1)):
                return choice


    def draw_input(self, msg):
        self._init_screen()
        curses.echo()
        msg_x = self._center_width(msg)
        msg_y = self.height // 2
        self.stdscr.addstr(msg_y, msg_x, msg)
        self.stdscr.refresh()
        inp = self.stdscr.getstr(msg_y, msg_x + len(msg))
        curses.noecho()
        return inp.decode('utf-8')



class Login(Window):
    def __init__(self):
        pass


class CreateAcc(Window):
    def __init__(self):
        pass
