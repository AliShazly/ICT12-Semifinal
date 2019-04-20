import curses
import json
import io

class Story:

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


    def _center_width(self, text):
        line_len = len(text.split('\n')[0])
        center = self.width // 2 - line_len // 2
        return (abs(center)+center)//2 # Turning negative numbers to 0


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
            start_y = self.height // 2
            for i in msg.split('\n'):
                start_x = self._center_width(i)
                stdscr.addstr(start_y, start_x, i)
                start_y += 2


    def _draw_border(self, stdscr):
        start_y_border = self.height//2 + self.height//5
        stdscr.addstr(start_y_border, 0, ('_' * self.width))


    def _draw_choices(self, stdscr, choices):
        start_y_choices = self.height//2 + self.height//4
        option_num = 1
        for i, j in zip(range(0, len(choices)*2, 2), choices):
            x = self._center_width(j)
            stdscr.addstr(start_y_choices + i, x, f'{option_num}: {j}')
            option_num += 1


    def _draw_art(self, stdscr, art):
        start_y_art = self.height//2 - self.height//3 - 4
        start_x_art = self._center_width(art)
        count = sorted([(i, art.count(i)) for i in set(art)], key=lambda x: x[1], reverse=True)
        background_char = count[0][0]
        art_formatted = art.replace(background_char, ' ')
        art_formatted = art_formatted.replace('\n', '\n' + (' ')*start_x_art)
        
        stdscr.addstr(start_y_art, start_x_art, art_formatted)


    def _draw_endscreen(self, stdscr, msg, gameover):
        self._init_terminal(stdscr)
        with io.open('endscreens.json', 'r', encoding='utf-8-sig') as infile:
            endscren = json.load(infile)
        art = endscren['gameover'] if gameover else endscren['gamewin']
        self._draw_art(stdscr, art)
        msg_x = self._center_width(msg)
        msg_y = self.height - self.height // 4
        stdscr.addstr(msg_y, msg_x, msg)
        stdscr.refresh()
        stdscr.getch()

    
    def _draw_input(self, stdscr, msg):
        self._init_terminal(stdscr)
        curses.echo()
        msg_x = self._center_width(msg)
        msg_y = self.height - self.height // 4
        stdscr.addstr(msg_y, msg_x, msg)
        stdscr.refresh()
        inp = stdscr.getstr(msg_y, msg_x + len(msg))
        curses.noecho()
        return inp.decode('utf-8')


    def _draw_scene(self, stdscr, k=1):
        self._init_terminal(stdscr)
        if self.art:
            self._draw_art(stdscr, self.art)
            self._draw_description(stdscr, self.desc)
        else:
            self._draw_description(stdscr, self.desc, center=True)
        self._draw_border(stdscr)
        self._draw_choices(stdscr, self.choices)

        stdscr.refresh()

        while True:
            k = stdscr.getch()
            if chr(k) in (str(i) for i in range(1, len(self.choices)+1)):
                return chr(k)

            if k == ord('q') or k == 27: # ESC
                raise SystemExit


    def draw_story(self, stdscr, previous_scene=None):

        # def log(msg):
        #     with open('log.txt', 'a+') as f:
        #         f.write(str(msg) + '\n')

        key = self._draw_scene(stdscr)
        try:
            next_scene = self.next_scenes['next_scenes'][str(key)]

            if 'gameover' in next_scene:
                msg = next_scene['gameover']
                return self._draw_endscreen(stdscr, msg, gameover=True)
                
            elif 'gamewin' in next_scene:
                msg = next_scene['gamewin']
                return self._draw_endscreen(stdscr, msg, gameover=False)

                
        except KeyError:
            pass

        try:
            if 'Go back' in self.next_scenes['next_scenes'][str(key)]['choices']:
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