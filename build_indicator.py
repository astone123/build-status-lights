from nanoleaf.nanoleaf import Nanoleaf
from nanoleaf.theme import Theme
from nanoleaf.tile import Tile
from status_color import StatusColor
from state import save_state, load_state


class BuildIndicator:

    def __init__(self, config, previous_state=None):
        self.nanoleaf = Nanoleaf(config)
        self.status_colors = StatusColor.map_statuses(config)
        self.project_tiles = {}
        self.project_map = self._assign_project_map(config, previous_state)

    def _assign_project_map(self, config, previous_state=None):
        if previous_state is None:
            previous_state = {}
        m = {}
        if len(config.projects) == 1:  # if there is only one project light the whole thing up
            m[config.projects[0].get('repo_url')] = self.nanoleaf.tiles
        else:
            t_id = 0
            for project, tile in zip(config.projects, self.nanoleaf.tiles):
                url = project.get('repo_url', None)
                branch = project.get('branch', 'develop')
                tiles = project.get('tile_ids', None)
                key = f"{url}-{branch}-{t_id}"
                value = previous_state.get(key, None)
                if value:
                    loaded_tiles = Tile.from_dict(value)
                    if tile:
                        m[key] = loaded_tiles
                        self.nanoleaf.update_tiles(loaded_tiles)
                    else:
                        m[key] = [tile]
                elif tiles is None:
                    m[key] = [tile]
                t_id = t_id + 1
        return m

    def update_theme(self, theme_data):
        self.nanoleaf.use_theme(theme_data)
        save_state(self.project_tiles)


    def update_project_status(self, project_repo_url, branch, status):
        r, g, b = self.status_colors[status]
        project_tiles = []
        for project, tiles in self.project_map.items():
            search_str = f"{project_repo_url}-{branch}"
            if search_str in project:
                project_tiles.append(tiles[0])
        if len(project_tiles) == 0:
            print(f"Invalid project url received! {project_repo_url}-{branch}")
            return
        for tile in project_tiles:
            tile.set_color(r, g, b)
        theme_data = self._build_theme_data()
        self.update_theme(theme_data)

    def _build_theme_data(self):
        theme = Theme.anim
        anim_string = self._build_anim_string()
        theme['animData'] = anim_string
        return theme

    def _build_anim_string(self):
        anim_string = f"{self.nanoleaf.panel_count}"
        for tile in self.nanoleaf.tiles:
            anim_string += f" {tile.get_theme_string()}"
        return anim_string
