from __future__ import print_function

import subprocess
import sys

box_characters = {
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
    def get_size(self, ):
        coords = subprocess.check_output(['stty', 'size']).decode().split()
        return [int(x) for x in coords]

    def clear_screen(self, ):
        print("\x1b[3J\x1b[2J", end="")

    def draw_rectangle(self, x1, y1, x2, y2, clear_center=True, box=box_characters, bold=set()):
        for side in bold:
            box = {k: chr(ord(v) + (k.find(side) + 1))
                   for k, v in box.items()}
        output = "\x1b[{y1};{x1}f{box[tl]}"
        output += "{box[t]}" * (x2 - x1 - 1)
        output += "{box[tr]}"
        for y in range(y1 + 1, y2):
            output += "\x1b[{y};{{x1}}f{{box[l]}}".format(y=y)
            if clear_center:
                output += " " * (x2 - x1 - 1)
            output += "\x1b[{y};{{x2}}f{{box[r]}}".format(y=y)
        output += "\x1b[{y2};{x1}f{box[bl]}"
        output += "{box[b]}" * (x2 - x1 - 1)
        output += "{box[br]}"

        print(output.format(x1=x1, y1=y1, x2=x2, y2=y2, box=box), end="")

        # print("\x1b[{};{}f{box[tl]}{}{box[tr]}".format(y1, x1,
        #                                                box['t'] * (x2 - x1 - 1), box=box), end="")
        # for y in range(y1 + 1, y2):
        #     print("\x1b[{};{}f{box[l]}{}{box[r]}".format(
        #         y, x1, " " * (x2 - x1 - 1), box=box), end="")
        # print("\x1b[{};{}f{box[bl]}{}{box[br]}".format(y2, x1,
        # box['b'] * (x2 - x1 - 1), box=box), end="")

    def flush(self):
        sys.stdout.flush()
