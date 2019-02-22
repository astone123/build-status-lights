from nanoleaf.nanoleaf import Nanoleaf
from nanoleaf.theme import Theme
from status_color import StatusColor
from server import save_state


class BuildIndicator:

    def __init__(self, config):
        self.nanoleaf = Nanoleaf(config)
        self.status_colors = StatusColor.map_statuses(config)
        self.project_tiles = {}
        self.project_map = self._assign_project_map(config)

    def _assign_project_map(self, config):
        m = {}
        if len(config.projects) == 1:  # if there is only one project light the whole thing up
            m[config.projects[0].get('repo_url')] = self.nanoleaf.tiles
        else:
            t_id = 0
            for project, tile in zip(config.projects, self.nanoleaf.tiles):
                url = project.get('repo_url', None)
                branch = project.get('branch', 'develop')
                tiles = project.get('tile_ids', None)
                if tiles is None:
                    m[f"{url}-{branch}-{t_id}"] = [tile]
                t_id = t_id + 1
        return m

    def update_theme(self, theme_data):
        self.nanoleaf.use_theme(theme_data)
        save_state(theme_data)


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
