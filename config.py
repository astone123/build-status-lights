import yaml

class Config:

    FILE_NAME = 'config.yaml'

    DEFAULT_COLORS = {
        'success': '00FF00',
        'in_progress': '00AAAA',
        'failure': 'FF0000'
    }

    def __init__(self):
        config_dict = Config._load()
        self.projects = config_dict.get('projects', [])
        self.nanoleaf = config_dict.get('nanoleaf', None)
        if self.nanoleaf is None:
            print('Update your config.yaml to include a nanoleaf ip and authorization token')
            exit(0)
        self.colors = config_dict.get('colors', Config.DEFAULT_COLORS)
        self.api_key = config_dict.get('api_key', None)
        self.ws_server_hostname = config_dict.get('ws_server_hostname', None)
        self.ws_server_port = config_dict.get('ws_server_port', 80)

    @classmethod
    def _load(cls):
        with open(Config.FILE_NAME, 'r') as stream:
            try:
                 return yaml.load(stream)
            except Exception:
                print('Unable to load configuration file, place a config.yaml in the root directory of this project')
                exit(0)