import asyncio

from opensky_api import OpenSkyApi


class PlaneState(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = OpenSkyApi()
        self.data = {}

    def fetch(self):
        data = self.api.get_states()
        if data is not None:
            self.data = data

    def plane_info(self, callsign):
        res = [s for s in self.data.states if s.callsign.startswith(callsign)]
        if not res:
            return None
        if len(res) == 1:
            return res[0]
        raise Exception(
            "Multiple matches for callsign {}: {}".format(callsign, res))

    async def update_loop(self):
        while True:
            self.fetch()
            await asyncio.sleep(11)
