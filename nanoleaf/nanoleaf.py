import requests

from nanoleaf.tile import Tile


class Nanoleaf:

    GET_TILE_ENDPOINT = 'panelLayout/layout/positionData'
    EFFECT_ENDPOINT = 'effects'

    def __init__(self, config):
        self.ip = config.nanoleaf.get('ip', None)
        authorization_token = config.nanoleaf.get('authorization_token', None)
        self.base_url = f"http://{self.ip}:16021/api/v1/{authorization_token}/"
        self.panel_ids = self.retrieve_tile_ids()
        self.panel_count = len(self.panel_ids)
        self.tiles = []
        for tile_id in self.panel_ids:
            self.tiles.append(Tile(tile_id))

    def retrieve_tile_ids(self):
        url = self.base_url + Nanoleaf.GET_TILE_ENDPOINT
        try:
            r = requests.get(url)
        except Exception:
            print('Unable to get tile information from nanoleaf')
            exit(0)

        response_json = r.json()
        if type(response_json) is list:
            panel_ids = [panel_data['panelId'] for panel_data in r.json()]
        else:
            panel_ids = [panel_data['panelId'] for panel_data in r.json()['positionData']]

        return panel_ids

    def use_theme(self, theme_data):
        url = self.base_url + Nanoleaf.EFFECT_ENDPOINT
        try:
            requests.put(url, json={'write': theme_data})
        except Exception:
            print('Unable to set theme on nanoleaf!')
            exit(0)


