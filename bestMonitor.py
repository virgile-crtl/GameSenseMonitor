import json, sys
from data import Data

class BestMonitor:
    i = 0
    game = "MONITOR"
    display_name = "Best Monitor"
    developer = "S2xLM2Z"

    def __init__(self):
        self.data = Data()
        try:
            file =open('bestMonitorEvents.json')
            self.events = json.load(file)
        except Exception as e:
            print(f"Error while opening the config file.\n{e}", end="")
            sys.exit()

    def get_game_info(self):
        return {
            "game": self.game,
            "game_display_name": self.display_name,
            "developer": self.developer
        }

    def get_event_to_bind(self):
        self.event_to_bind = self.events.get("event_to_bind", [])
        for event in self.event_to_bind:
            event["game"] = self.game
        return self.event_to_bind

    def get_event_to_register(self):
        self.event_to_register = self.events.get("event_to_register", [])
        for event in self.event_to_register:
            event["game"] = self.game
        return self.event_to_register

    def get_all_monitor_info(self):
        self.i += 1
        return {
            "game": self.game,
            "event": "ALL_MONITOR_INFO",
            "data": {
                "value": self.i,
                "frame": {
                    "cpu_temp": self.data.get_cpu_temp()+"°C",
                    "gpu_temp": self.data.get_gpu_temp()+"°C",
                    "ram_usage": self.data.get_ram_usage(),
                }
            }
        }

    def get_game(self):
        return {"game": self.game}

    def get_timer(self):
        return self.i

    def reset_timer(self):
        self.i = 0
        return self.i



