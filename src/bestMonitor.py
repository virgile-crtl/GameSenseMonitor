import json, sys
from data import Data

class BestMonitor:
    timer = 0
    game = "MONITOR"
    display_name = "Best Monitor"
    developer = "LM2Z"


    def __init__(self):
        try :
            self.data = Data()
        except Exception as e:
            raise e
        try:
            self.config_file =open('C:\\Users\\virgile\\Documents\\Dev\\Better-Monitoring\\assets\\config\\bestMonitorInfos.json', 'r+')
            # file =open('C:\\Program Files\\BestMonitor\\dist\\assets\\config\\bestMonitorInfos.json')
            self.infos= json.load(self.config_file)
        except Exception as e:
            my_e = type(e)(f"Error while loading the config file.\n{e}")
            raise my_e from e

    def __del__(self):
        try:
            self.config_file.seek(0)
            json.dump(self.infos, self.config_file, indent=4)
            self.config_file.truncate()
            self.config_file.close()
        except Exception as e:
            print(f"Error while saving the config file.\n{e}")
            # show_error_popup("Error while saving the config file.\n"+
            # "If data has been modified, it may not have been saved.", f"{e}")

    def check_config_file(self):
        self.event_to_bind = self.infos.get("event_to_bind", [])
        if not self.event_to_bind or self.event_to_bind == []:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the events to bind.\n")
        self.event_to_register = self.infos.get("event_to_register", [])
        if not self.event_to_register or self.event_to_register == []:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the events to register.\n")
        if not self.infos["app_config_values"]["refresh_rate"]:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the refresh rate.\n")
        if not self.infos["app_config_values"]["display_volume_time"]:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the display volume time.\n")
        if not self.infos["app_config_values"]["display_info_time"]:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the display info time.\n")
        if not self.infos["app_config_values"]["current_event"]:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the current event.\n")
        i = 0
        for event in self.event_to_register:
            if event.get("event", "") == self.infos["app_config_values"]["current_event"]:
                i += 1
        if i == 0:
            raise Exception("The configuration file seems corrupted.\n"+
            "The current event is not in the list of events.\n")


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

    def get_info_to_send(self):
        if self.infos["app_config_values"]["current_event"] == "ALL_MONITOR_INFO":
            return self.get_all_monitor_info()
        if self.infos["app_config_values"]["current_event"] == "HOUR_TEMP_INFO":
            return self.get_hour_temp_info()
        return {}

    def get_all_monitor_info(self):
        self.timer += 1
        return {
            "game": self.game,
            "event": "ALL_MONITOR_INFO",
            "data": {
                "value": self.timer,
                "frame": {
                    "cpu_temp": self.data.get_cpu_temp(),
                    "gpu_temp": self.data.get_gpu_temp(),
                    "ram_usage": self.data.get_ram_usage()
                }
            }
        }

    def get_hour_temp_info(self):
        self.timer += 1
        return {
            "game": self.game,
            "event": "HOUR_TEMP_INFO",
            "data": {
                "value": self.timer,
                "frame": {
                    "hour": self.data.get_hour(),
                    "cpu_temp": self.data.get_cpu_temp(),
                    "gpu_temp": self.data.get_gpu_temp()
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

    def get_refresh_rate(self) -> int:
        return self.infos["app_config_values"]["refresh_rate"]

    def set_refresh_rate(self, value):
        self.infos["app_config_values"]["refresh_rate"] = value
        return self.infos["app_config_values"]["refresh_rate"]

    def get_display_vol(self) -> int:
        return self.infos["app_config_values"]["display_volume_time"]

    def set_display_vol(self, value):
        self.infos["app_config_values"]["display_volume_time"] = value
        return self.infos["app_config_values"]["display_volume_time"]

    def get_display_info(self) -> int:
        return self.infos["app_config_values"]["display_info_time"]

    def set_display_info(self, value):
        self.infos["app_config_values"]["display_info_time"] = value
        return self.infos["app_config_values"]["display_info_time"]




