import asyncio

from utils import Terminal
from plane_tracker import PlaneState


async def render(term, tracker):
    frame = 0
    while True:
        frame += 1
        r, c = term.get_size()
        term.clear_screen()
        term.hide_cursor()
        term.draw_rectangle((1, 1, c, r), bold={"t", "l", "b", "r"})
        for pinf in tracker.data.states:
            if pinf.longitude and pinf.latitude:
                x = int((c - 2) * (pinf.longitude / 360 + .5))
                y = int((r - 2) * (-pinf.latitude / 180 + .5))
                term.move_to(x + 1, y + 1)
                term.send_data("O")
        term.flush()
        await asyncio.sleep(1 / 30)


def main():
    loop = asyncio.get_event_loop()
    tracker = PlaneState()
    tracker.fetch()
    loop.create_task(tracker.update_loop())
    term = Terminal(cache=True)
    loop.create_task(render(term, tracker))
    try:
        loop.run_forever()
    finally:
        loop.stop()


if __name__ == "__main__":
    main()
