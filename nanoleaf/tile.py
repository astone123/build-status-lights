class Tile:

    @staticmethod
    def from_dict(t_list):
        tile_array = []
        for obj in t_list:
            t_id = obj.get('tile_id', None)
            color_array = obj.get('color_data', None)
            if t_id and color_array:
                tile_array.append(Tile(t_id, color_array))
        if tile_array:
            return tile_array
        return None

    def __init__(self, tile_id, color=None):
        if color is None:
            color = [0, 0, 0, 0, 0]
        self.tile_id = tile_id
        self.color_data = color


    def set_color(self, r, g, b):
        self.color_data[0] = r
        self.color_data[1] = g
        self.color_data[2] = b

    def stringify_color_data(self):
        return ' '.join(str(color_elem) for color_elem in self.color_data)

    def get_theme_string(self):
        return f"{self.tile_id} 1 {self.stringify_color_data()}"

