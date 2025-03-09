import json, sys, os

class BestMonitor:
    timer = 0
    game = "MONITOR"
    display_name = "Best Monitor"
    developer = "LM2Z"
    infos = {}


    def __init__(self, config):
        self.event_to_register = config["event_to_register"]
        self.event_to_bind = config["event_to_bind"]


    def get_game_info(self):
        return {
            "game": self.game,
            "game_display_name": self.display_name,
            "developer": self.developer
        }

    def get_event_to_bind(self):
        for event in self.event_to_bind:
            event["game"] = self.game
        return self.event_to_bind

    def get_event_to_register(self):
        for event in self.event_to_register:
            event["game"] = self.game
        return self.event_to_register

    def get_info_to_send(self, data, current_event):
        if current_event == "ALL_MONITOR_INFO":
            return self.get_all_monitor_info(data)
        if current_event == "HOUR_TEMP_INFO":
            return self.get_hour_temp_info(data)
        return {}

    def get_all_monitor_info(self, data):
        self.timer += 1
        return {
            "game": self.game,
            "event": "ALL_MONITOR_INFO",
            "data": {
                "value": self.timer,
                "frame": {
                    "cpu_temp": data["cpu_temp"],
                    "gpu_temp": data["gpu_temp"],
                    "ram_usage": data["ram_usage"]
                }
            }
        }

    def get_hour_temp_info(self, data):
        self.timer += 1
        return {
            "game": self.game,
            "event": "HOUR_TEMP_INFO",
            "data": {
                "value": self.timer,
                "frame": {
                    "hour": data["hour"],
                    "cpu_temp": data["cpu_temp"],
                    "gpu_temp": data["gpu_temp"]
                }
            }
        }

    def get_game(self):
        return {"game": self.game}

    def get_timer(self) -> int:
        return self.timer

    def set_timer(self, value):
        self.timer = value
        return self.timer

    def get_events(self):
        return {
            "event_to_bind": self.event_to_bind,
            "event_to_register": self.event_to_register
        }