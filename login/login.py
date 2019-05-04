import os
import curses
import binascii
import hashlib
import json


def hash_salt(pwd, salt=None):
    if salt is None:
        random_bytes = os.urandom(8)
        salt = binascii.hexlify(random_bytes).decode('ascii')
    hash_bytes = hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), salt.encode('utf-8'), 100000)
    hashed_pwd = binascii.hexlify(hash_bytes).decode('utf-8')
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
        return (abs(center) + center) // 2  # Turning negative numbers to 0

    def _draw_input(self, msg, y_val, x_val, echo=True):
        if echo:
            curses.echo()
        self.stdscr.addstr(y_val, x_val, msg)
        self.stdscr.refresh()
        inp = self.stdscr.getstr(y_val, x_val + len(msg))
        curses.noecho()
        return inp.decode('utf-8')

    def draw_options(self, *args, separation=5):
        self._init_screen()
        start_y_choices = self.height//2
        y_step = range(0, len(args) * separation, separation)
        option_nums = range(1, len(args) + 1)

        for step, option, num in zip(y_step, args, option_nums):
            x_val = self._center_width(option)
            self.stdscr.addstr(start_y_choices + step, x_val, f'{num}: {option}')
        while True:
            choice = chr(self.stdscr.getch())
            if choice in (str(i) for i in range(1, len(args) + 1)):
                return choice

    def multiple_inputs(self, *args, separation=5):
        self._init_screen()
        start_y_choices = self.height//2
        y_step = range(0, len(args) * separation, separation)

        inputs = []
        for step, option, in zip(y_step, args):
            x_val = self._center_width(option)
            y_val = start_y_choices + step
            if 'password' in option.lower():
                inp = self._draw_input(option, y_val, x_val, echo=False)
            else:
                inp = self._draw_input(option, y_val, x_val)
            inputs.append(inp)

        return inputs

    def draw_message(self, msg, error=False):
        self._init_screen()
        if error:
            msg = f'ERROR: {msg} | Press enter to try again...'
        self.stdscr.addstr(self.height // 2, self._center_width(msg), msg)
        msg_quit = 'Press "Q" to quit'
        self.stdscr.addstr(self.height // 2 + 5, self._center_width(msg_quit), msg_quit)
        if chr(self.stdscr.getch()) == 'q':
            raise SystemExit


class Login(Window):

    def authenticate_user(self, path='./users.json'):
        username, password = self.multiple_inputs(
            'Enter Username: ',
            'Enter Password: '
        )

        with open(path, 'r') as f:
            data = json.load(f)

        try:
            if username in data.keys():
                hashed_pwd, salt = data[username]
            else:
                raise KeyError('User not found.')

            if hash_salt(password, salt)[0] != hashed_pwd:
                raise ValueError('Password is incorrect.')

        except (ValueError, KeyError) as e:
            self.draw_message(e, error=True)
            return self.authenticate_user()

        return True


class CreateAcc(Window):

    def new_user(self, path='./users.json'):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = {}

        username, pwd, confirm_pwd = self.multiple_inputs(
            'Enter Username: ',
            'Enter Password: ',
            'Confirm Password: '
        )

        if username in data.keys():
            self.draw_message('Username already exists.', error=True)
            return self.new_user()

        if pwd != confirm_pwd:
            self.draw_message('Passwords do not match.', error=True)
            return self.new_user()

        if not all((i.strip() for i in (username, pwd))):
            self.draw_message('Username or password is empty.', error=True)
            return self.new_user()

        hashed_pwd, salt = hash_salt(pwd)
        data[username] = [hashed_pwd, salt]

        with open(path, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4)


def main(stdscr):
    main_win = Window(stdscr)
    choice = main_win.draw_options('Login', 'Create Account')
    if choice == '1':
        login_win = Login(stdscr)
        login_win.authenticate_user()
        login_win.draw_message('Success!')

    else:
        create_acc_win = CreateAcc(stdscr)
        create_acc_win.new_user()
        create_acc_win.draw_message('Success!')


curses.wrapper(main)
