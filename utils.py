from __future__ import print_function

import subprocess
import sys

BOX_CHARS = {
    "t": u"\u2500",
    "b": u"\u2500",
    "l": u"\u2502",
    "r": u"\u2502",
    "tl": u"\u250C",
    "tr": u"\u2510",
    "bl": u"\u2514",
    "br": u"\u2518",
}


class Terminal(object):
    def __init__(self, cache=False, *args, **kwargs):
        super(Terminal, self).__init__(*args, **kwargs)
        self.cache = cache
        self.data = ""

    def hide_cursor(self):
        self.send_data("\x1b[?25l")

    def get_size(self):
        coords = subprocess.check_output(['stty', 'size']).decode().split()
        return [int(x) for x in coords]

    def clear_screen(self):
        self.send_data("\x1b[3J\x1b[2J")

    def draw_rectangle(self,
                       coords,
                       clear_center=True,
                       box=BOX_CHARS,
                       bold=set()):
        for side in bold:
            box = {k: chr(ord(v) + (k.find(side) + 1))
                   for k, v in box.items()}
        output = "\x1b[{y1};{x1}f{box[tl]}"
        output += "{box[t]}" * (coords[2] - coords[0] - 1)
        output += "{box[tr]}"
        for ycoord in range(coords[1] + 1, coords[3]):
            output += "\x1b[{y};{{x1}}f{{box[l]}}".format(y=ycoord)
            if clear_center:
                output += " " * (coords[2] - coords[0] - 1)
            output += "\x1b[{y};{{x2}}f{{box[r]}}".format(y=ycoord)
        output += "\x1b[{y2};{x1}f{box[bl]}"
        output += "{box[b]}" * (coords[2] - coords[0] - 1)
        output += "{box[br]}"

        print(output.format(x1=coords[0], y1=coords[1],
                            x2=coords[2], y2=coords[3], box=box), end="")

    def move_to(self, x, y):
        self.send_data("\x1b[{};{}f".format(y, x))

    def send_data(self, data):
        if self.cache:
            self.data += data
        else:
            print(self.data, end="")

    def flush(self):
        if self.cache:
            print(self.data, end="")
        sys.stdout.flush()
        self.data = ""
