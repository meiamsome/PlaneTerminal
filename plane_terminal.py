from time import sleep

from utils import Terminal


def render(term, frame):
    r, c = term.get_size()
    term.clear_screen()
    term.draw_rectangle(1, 1, c, r, bold={"t", "l", "b", "r"})
    term.draw_rectangle(4, 4, c >> 1, r >> 1, bold=[
        {"t", "l"},
        {"t", "r"},
        {"r", "b"},
        {"b", "l"},
    ][(frame >> 2) % 4])
    term.flush()


if __name__ == "__main__":
    term = Terminal()
    frame = 0
    try:
        while True:
            render(term, frame)
            sleep(1 / 30)
            frame += 1
    except Exception as e:
        term.clear_screen()
        raise
