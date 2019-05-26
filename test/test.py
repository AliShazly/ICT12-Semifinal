import curses
import json


class Question:
    def __init__(self, problem: str, answer: str, choices=[]):
        self.problem = problem
        self.answer = answer
        self.choices = choices
        if self.choices is None:
            self.choices = []


class Page:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.score = []

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
        line_len = len(text.split("\n")[0])
        center = self.width // 2 - line_len // 2
        return (abs(center) + center) // 2  # Turning negative numbers to 0

    def _draw_problem(self, question):
        y_pos = 0
        question_list = question.split(" ")

        for i, j in enumerate(question_list):
            y_pos += len(j) + 1
            if y_pos >= self.width:
                question_list[i] = f"\n{question_list[i]}"
                y_pos = 0
        msg = " ".join(question_list)

        start_y = self.height // 4
        for i in msg.split("\n"):
            start_x = self._center_width(i)
            self.stdscr.addstr(start_y, start_x, i)
            start_y += 2

    def _draw_seperator(self):
        start_y_border = self.height // 2 + self.height // 10
        self.stdscr.addstr(start_y_border, 0, ("_" * self.width))

    def _draw_choices(self, choices, separation=3):
        start_y_choices = self.height // 2 + self.height // 5
        y_step = range(0, len(choices) * separation, separation)
        option_nums = ["A", "B", "C", "D", "E", "F"]

        for step, option, num in zip(y_step, choices, option_nums):
            x_val = self._center_width(option)
            self.stdscr.addstr(start_y_choices + step, x_val, f"{num}: {option}")

        while True:
            k = self.stdscr.getch()
            if chr(k).upper() in option_nums[: len(choices)]:
                idx = option_nums.index(chr(k).upper())
                return choices[idx]

            if k == ord("q") or k == 27:  # ESC
                raise SystemExit

    def _draw_input(self, msg):
        curses.echo()
        msg_x = self._center_width(msg)
        msg_y = self.height - self.height // 4
        self.stdscr.addstr(msg_y, msg_x, msg)
        self.stdscr.refresh()
        inp = self.stdscr.getstr(msg_y, msg_x + len(msg))
        curses.noecho()
        return inp.decode("utf-8")

    def _draw_mult_choice(self, question):
        self._init_screen()
        self._draw_problem(question.problem)
        self._draw_seperator()
        choice = self._draw_choices(question.choices)
        if choice.lower().strip() == question.answer.lower().strip():
            self.score.append(True)
        else:
            self.score.append(False)

    def _draw_short_answer(self, question):
        self._init_screen()
        self._draw_problem(question.problem)
        self._draw_seperator()

        try:
            int(question.answer)
            ans_type = "integer"
        except ValueError:
            ans_type = "string"

        answer = self._draw_input(f"Enter answer ({ans_type}): ")
        if answer.lower().strip() == question.answer.lower().strip():
            self.score.append(True)
        else:
            self.score.append(False)

    def draw_test(self, question_list):
        for question in question_list:
            if question.choices:  # Multiple choice
                self._draw_mult_choice(question)
            else:
                self._draw_short_answer(question)

        correct = self.score.count(True)
        percentage = round(correct / len(question_list), 2) * 100
        self._init_screen()
        self._draw_problem(
            f"You got {correct} question(s) right out of {len(question_list)}.\nThat is {percentage}%"
        )
        self.stdscr.getch()


def main(stdscr):
    page = Page(stdscr)
    with open("test.json", "r") as f:
        test = json.load(f)
    questions = [Question(*question) for question in test]
    page.draw_test(questions)


curses.wrapper(main)
