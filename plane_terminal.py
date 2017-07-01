import asyncio

from terminal import Terminal
from plane_tracker import PlaneState
from PIL import Image


async def render(term, tracker):
    frame = 0
    while True:
        frame += 1
        r, c = term.get_size()
        # term.clear_screen()
        term.hide_cursor()
        term.draw_rectangle(
            (0, 0, c - 1, r - 1),
            bold={"t", "l", "b", "r"},
            color=(255, 255, 255)
        )
        for pinf in tracker.data.states:
            if pinf.longitude and pinf.latitude:
                x = int((c - 1) * (pinf.longitude / 360 + .5))
                y = int((r - 1) * (-pinf.latitude / 180 + .5))
                term.data[y][x][0] = u"\u2022"
        term.output()
        await asyncio.sleep(1 / 30)


def main():
    with Terminal(((255, 0, 0), (0, 0, 0))) as term:
        loop = asyncio.get_event_loop()
        tracker = PlaneState()
        tracker.fetch()
        loop.create_task(tracker.update_loop())
        img = Image.open('img/map.jpg')
        y, x = term.get_size()
        term.set_background_image(
            img, (0, 0, x - 1, y - 1), resample=Image.LANCZOS)
        loop.create_task(render(term, tracker))
        try:
            loop.run_forever()
        finally:
            loop.stop()


if __name__ == "__main__":
    main()
