class Tile:

    def __init__(self, tile_id):
        self.tile_id = tile_id
        self.color_data = [0,0,0,0,0]

    def set_color(self, r, g, b):
        self.color_data[0] = r
        self.color_data[1] = g
        self.color_data[2] = b

    def stringify_color_data(self):
        return ' '.join(str(color_elem) for color_elem in self.color_data)

    def get_theme_string(self):
        return f"{self.tile_id} 1 {self.stringify_color_data()}"