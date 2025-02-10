import requests, os, json

class Endpoints:
    REGISTER_GAME = "/game_metada"
    REMOVE_GAME = "/remove_game"
    REGISTER_EVENT = "/register_game_event"
    BIND_EVENT = '/bind_game_event'
    REMOVE_EVENT = '/remove_game_event'
    SEND_EVENT = '/game_event'
    HEARTBEAT = '/game_heartbeat'

class GameSense():

    def __init__(self, game_name, display_name, developer):
        self.address = self.find_port()
        self.game_name = game_name
        self.display_name = display_name
        self.developer = developer
        self.endpoint = Endpoints()
        self.register_game()
        self.bind_event()

    def find_port(self):
        path = os.path.expandvars(
            r'%programdata%\SteelSeries\SteelSeries Engine 3\coreProps.json')
        return 'http://'+json.load(open(path))['address']
    
    def register_game(self):
        requests.post(self.address + self.endpoint.REGISTER_GAME, json = {
            "game": self.game_name,
            "game_display_name": self.display_name,
            "developer": self.developer,
        })

    def register_event(self):
        requests.post(self.address + self.endpoint.REGISTER_EVENT, json = {
            "game": self.game_name,
            "event":"HW",
            "value_optional": True
        })

    def bind_event(self):
        requests.post(self.address + self.endpoint.BIND_EVENT, json = {
            "game": self.game_name,
            "event": "HW",
            "handlers": [{
                "device-type":"screened",
                "mode":"screen",
                "zone":"one",
                "datas": [{
                    "has-text":True,
                    "context-frame-key":"custom-text"
                }]
            }]
        })

    def send_event(self, data):
        requests.post(self.address + self.endpoint.SEND_EVENT, json = {
            "game": self.game_name,
            "event": "HW",
            "data": data
        })