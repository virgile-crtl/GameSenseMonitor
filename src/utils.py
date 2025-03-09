import json, os, sys
from dotenv import load_dotenv # type: ignore

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # Si exécuté en mode PyInstaller
        base_path = sys._MEIPASS
    else:
        # Mode script normal (non compilé)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def saved_config(popUp, config):
    try:
        config_file =open(get_resource_path("assets\\config\\bestMonitorInfos.json"), 'r+')
        config_file.seek(0)
        json.dump(config, config_file, indent=4)
        config_file.truncate()
        config_file.close()
    except Exception as e:
        print(f"Error while saving the config file.\n{e}")
        popUp.error("Error while saving the config file.\n"+
        "If data has been modified, it may not have been saved.", f"{e}")
        sys.exit(1)

def connection_with_sonar(bestMonitor, gameSense, popUp):
    try:
        gameSense.register_game(bestMonitor.get_game_info())
        for event in bestMonitor.get_event_to_register():
            gameSense.register_event(event)
        for event in bestMonitor.get_event_to_bind():
            gameSense.bind_event(event)
    except Exception as e:
        popUp.error_restart("Error during connection with Sonar.\nSonar must be running." +
        "Verify if it is running in the background.\nOtherwise, start it and click on 'Restart'.", f"{e}")
        sys.exit(1)

def load_config_files():
        config_file =open(get_resource_path("assets\\config\\bestMonitorInfos.json"), 'r+')
        infos = (json.load(config_file))
        config_file.close()
        event_to_bind = infos.get("event_to_bind", [])
        event_to_register = infos.get("event_to_register", [])
        if not event_to_bind or event_to_bind == []:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the events to bind.\n")
        if not event_to_register or event_to_register == []:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the events to register.\n")
        if not infos["app_config_values"]["refresh_rate"]:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the refresh rate.\n")
        if not "display_volume_time" in infos["app_config_values"]:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the display volume time.\n")
        if not "display_info_time" in infos["app_config_values"]:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the display info time.\n")
        if not "current_event" in infos["app_config_values"]:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the current event.\n")
        i = 0
        for event in event_to_register:
            if event.get("event", "") == infos["app_config_values"]["current_event"]:
                i += 1
        if i == 0:
            raise Exception("The configuration file seems corrupted.\n"+
            "The current event is not in the list of events.\n")
        return infos