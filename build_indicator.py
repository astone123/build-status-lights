from nanoleaf.nanoleaf import Nanoleaf
from nanoleaf.theme import Theme
from status_color import StatusColor


class BuildIndicator:

    def __init__(self, config):
        self.nanoleaf = Nanoleaf(config)
        self.status_colors = StatusColor.map_statuses(config)
        self.project_tiles = {}
        self.project_map = self._assign_project_map(config)

    def _assign_project_map(self, config):
        m = {}
        if len(config.projects) == 1: # if there is only one project light the whole thing up
            m[config.projects[0].get('repo_url')] = self.nanoleaf.tiles
        else:
            for project, tile in zip(config.projects, config.nanoleaf.tiles):
                url = project.get('repo_url', None)
                tiles = project.get('tile_ids', None)
                if tiles is None:
                    m[url] = tile
        return m


    def update_project_status(self, project_repo_url, status):
        r,g,b = self.status_colors[status]
        project_tiles = self.project_map.get(project_repo_url, [])
        if len(project_tiles) == 0:
            print(f"Invalid project url received! {project_repo_url}")
            return
        for tile in project_tiles:
            tile.set_color(r,g,b)
        theme_data = self._build_theme_data()
        self.nanoleaf.use_theme(theme_data)

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
