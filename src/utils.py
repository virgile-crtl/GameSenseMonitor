import json, os, sys
from dotenv import load_dotenv # type: ignore

def saved_config(popUp, config):
    try:
        config_file =open(os.getenv("CONFIG_FILE_PATH"), 'r+')
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

def load_env():
    try:
        if os.getenv('ENV', 'dev') == 'prod':
            load_dotenv('.env.prod')
        else:
            load_dotenv('.env.dev')
    except Exception as e:
            my_e = type(e)(f"Error while loading the env file.\n{e}")
            raise my_e from e

def load_config_files():
        config_file =open(os.getenv("CONFIG_FILE_PATH"), 'r+')
        infos = (json.load(config_file))
        config_file.close()
        event_to_bind = infos.get("event_to_bind", [])
        if not event_to_bind or event_to_bind == []:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the events to bind.\n")
        event_to_register = infos.get("event_to_register", [])
        if not event_to_register or event_to_register == []:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the events to register.\n")
        if not infos["app_config_values"]["refresh_rate"]:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the refresh rate.\n")
        if not infos["app_config_values"]["display_volume_time"]:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the display volume time.\n")
        if not infos["app_config_values"]["display_info_time"]:
            raise Exception("The configuration file seems corrupted.\n"+
            "Error while getting the display info time.\n")
        if not infos["app_config_values"]["current_event"]:
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