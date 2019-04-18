import curses
import json
import io
import sys

class Story:
    # def __init__(self, desc, choices, next_scenes=None, art=None, height=0, width=0):
    #     self.desc = desc
    #     self.choices = choices
    #     self.art = art
    #     self.next_scenes = next_scenes
    #     self.height = height
    #     self.width = width

    def __init__(self, story_dict, height=0, width=0):
        self.desc = story_dict['desc']
        self.choices = story_dict['choices']
        self.art = story_dict['art']
        self.next_scenes = story_dict
        self.height = height
        self.width = width

    def _init_terminal(self, stdscr):
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


    def _draw_description(self, stdscr, desc, center=False):
        y_pos = 0
        desc_list = desc.split(' ')

        for i, j in enumerate(desc_list):
            y_pos += len(j) + 1
            if y_pos >= self.width:
                desc_list[i] = f'\n{desc_list[i]}'
                y_pos = 0
        msg = ' '.join(desc_list)

        if not center:
            stdscr.addstr(0, 0, msg)
        else:
            start_x, start_y = 0, self.height//2 # TODO: Center x val
            print(start_x, start_y, len(msg), msg)
            stdscr.addstr(start_y, start_x, msg)


    def _draw_border(self, stdscr):
        start_y_border = self.height//2 + self.height//5
        stdscr.addstr(start_y_border, 0, ('_' * self.width))


    def _draw_choices(self, stdscr, choices):
        start_y_choices = self.height//2 + self.height//4
        option_num = 1
        for i, j in zip(range(0, len(choices)*2, 2), choices):
            x = self.width//2 - len(j)//2
            stdscr.addstr(start_y_choices + i, x, f'{option_num}: {j}')
            option_num += 1


    def _draw_art(self, stdscr, art):
        start_y_art = self.height//2 - self.height//3 - 4

        line_len = 0
        for i in art:
            if i == '\n':
                break
            line_len +=1
        
        start_x_art = self.width//2 - line_len//2
        count = sorted([(i, art.count(i)) for i in set(art)], key=lambda x: x[1], reverse=True)
        background_char = count[0][0]
        art_formatted = art.replace(background_char, ' ')
        art_formatted = art_formatted.replace('\n', '\n' + (' ')*start_x_art)
        
        stdscr.addstr(start_y_art, start_x_art, art_formatted)


    def _draw_gameover(self, stdscr, msg='Game over.'):
        self._init_terminal(stdscr)
        self._draw_art(stdscr, open('gameover.txt').read())
        msg_x, msg_y = self.width//2 - len(msg)//2, self.height - self.height//4
        stdscr.addstr(msg_y, msg_x, msg)
        stdscr.refresh()
        stdscr.getch()

    def _draw_scene(self, stdscr, k=1):
        self._init_terminal(stdscr)
        if self.art:
            self._draw_art(stdscr, self.art)
            self._draw_description(stdscr, self.desc)
        else:
            self._draw_description(stdscr, self.desc, center=True)
        self._draw_border(stdscr)
        self._draw_choices(stdscr, self.choices)

        if k == ord('q') or k == 27: # ESC
            raise SystemExit

        stdscr.refresh()
        k = stdscr.getch()

        if chr(k) in (str(i) for i in range(1, len(self.choices)+1)):
            return chr(k)

        self._draw_scene(stdscr, k)


    def draw_story(self, stdscr, previous_scene=None):
        key = self._draw_scene(stdscr)

        try:
            if 'gameover' in self.next_scenes['next_scenes'][str(key)]:
                msg = self.next_scenes['next_scenes'][str(key)]['gameover']
                self._draw_gameover(stdscr, msg)
                return
        except KeyError:
            pass

        try:
            if self.next_scenes['next_scenes'][str(key)]['choices'] == ['Go back']:
                previous_scene = self.next_scenes
            self.next_scenes = self.next_scenes['next_scenes'][str(key)]
        except KeyError:
            self.next_scenes = previous_scene
        
        self.desc = self.next_scenes['desc']
        self.choices = self.next_scenes['choices']
        self.art = self.next_scenes['art']
        return self.draw_story(stdscr, previous_scene)


with io.open('paths.json', 'r', encoding='utf-8-sig') as infile:
    amnesia_dict = json.load(infile)


amnesia = Story(amnesia_dict)
curses.wrapper(amnesia.draw_story)