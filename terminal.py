from time import sleep

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


def get_terminal_size():
    coords = subprocess.check_output(['stty', 'size']).decode().split()
    return [int(x) for x in coords]


class Terminal(object):
    def __init__(self, colors=((255, 255, 255), (0, 0, 0)), *args, **kwargs):
        super(Terminal, self).__init__(*args, **kwargs)
        self.size = [0, 0]
        self.data = []
        self.cache = ""
        self.default_colors = colors

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.clear_screen(colors=(None, None))
        self.output()
        self.send_data("\x1b[0f\x1b[0m")
        self.flush()

    def hide_cursor(self):
        self.send_data("\x1b[?25l")

    def get_size(self):
        new_size = get_terminal_size()
        if self.size != new_size:
            self.size = new_size
            self.clear_screen()
        return self.size

    def clear_screen(self, colors=None):
        if colors is None:
            colors = self.default_colors
        self.data = [
            [
                [None, colors[0], colors[1]] for x in range(self.size[1])
            ] for y in range(self.size[0])
        ]

    def output(self):
        current_colours = [None, None]
        self.send_data("\x1b[0m")
        for y in range(self.size[0]):
            self.send_data("\x1b[{}f".format(y + 1))
            for x in range(self.size[1]):
                letter, fgcol, bgcol = self.data[y][x]
                if bgcol is not None and bgcol != current_colours[1]:
                    current_colours[1] = bgcol
                    self.send_data("\x1b[48;2;{};{};{}m".format(*bgcol))
                if fgcol is not None and fgcol != current_colours[0]:
                    current_colours[0] = fgcol
                    self.send_data("\x1b[38;2;{};{};{}m".format(*fgcol))
                self.send_data(" " if letter is None else letter)
        self.flush()

    def send_data(self, data):
        self.cache += data

    def flush(self):
        print(self.cache, end="")
        self.cache = ""

    def set_character(self, x, y, char=None, fg=None, bg=None):
        if char is not None:
            self.data[y][x][0] = char
        if fg is not None:
            self.data[y][x][1] = fg
        if bg is not None:
            self.data[y][x][2] = bg

    def draw_rectangle(self,
                       coords,
                       box=BOX_CHARS,
                       bold=set(),
                       color=None):
        for side in bold:
            box = {k: chr(ord(v) + (k.find(side) + 1))
                   for k, v in box.items()}
        self.set_character(coords[0], coords[1], box["tl"], fg=color)
        self.set_character(coords[2], coords[1], box["tr"], fg=color)
        self.set_character(coords[0], coords[3], box["bl"], fg=color)
        self.set_character(coords[2], coords[3], box["br"], fg=color)
        for y in range(coords[1] + 1, coords[3]):
            self.set_character(coords[0], y, box["l"], fg=color)
            self.set_character(coords[2], y, box["r"], fg=color)
        for x in range(coords[0] + 1, coords[2]):
            self.set_character(x, coords[1], box["t"], fg=color)
            self.set_character(x, coords[3], box["b"], fg=color)

    def set_background_image(self, image, coords=None, resample=None):
        if coords is None:
            coords = (0, 0, self.size[1], self.size[0])
        resized = image.resize(
            (coords[2] - coords[0] + 1, coords[3] - coords[1] + 1),
            resample=resample)
        for y in range(coords[1], coords[3] + 1):
            for x in range(coords[0], coords[2] + 1):
                self.data[y][x][2] = resized.getpixel(
                    (x - coords[0], y - coords[1]))
