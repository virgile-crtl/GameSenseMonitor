import requests

class GameSense:
    adress = "http://localhost:"

    def __init__(self, port):
        self.adress += port
        requests.post(self.adress + "/game_metada", json = {
            "game": "MONITOR",
            "game_display_name": "Best Monitor",
            "developer": "S2xLM2Z",
        })
        self.bind_event()

    def register_event(self):
        requests.post(self.adress + "/register_game_event", json = {
            "game":"MONITOR",
            "event":"HW",
            "value_optional": True
        })

    def bind_event(self):
        requests.post(self.adress + "/bind_game_event", json = {
            "game": "MONITOR",
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
        requests.post(self.adress + "/game_event", json = {
            "game": "MONITOR",
            "event": "HW",
            "data": data
        })