class StatusColor:

    @staticmethod
    def map_statuses(self, config):
        return {
            'INPROGRESS': StatusColor.hex_to_rgb(config.colors.in_progress),
            'FAILED': StatusColor.hex_to_rgb(config.colors.failure),
            'SUCCESSFUL': StatusColor.hex_to_rgb(config.colors.success)
        }

    @staticmethod
    def hex_to_rgb(hex_string):
        if '#' in hex_string:
            hex_string = hex_string[1:]
            return tuple(int(hex_string[i:i + 2], 16) for i in (0, 2, 4))
        return tuple(int(hex_string[i:i + 2], 16) for i in (0, 2, 4))