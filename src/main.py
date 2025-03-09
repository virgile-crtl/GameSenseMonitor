import time
import threading
from pystray import Icon, MenuItem, Menu
from pystray import MenuItem as item
from PIL import Image
from gameSense import GameSense
from bestMonitor import BestMonitor
import sys, ctypes
import tkinter as tk
from tkinter import scrolledtext
import traceback
import ctypes
from popUp import Popup
import os
from dotenv import load_dotenv # type: ignore
import sys
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import multiprocessing
from setting import Setting
from data import Data
import json

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

def main_loop(bestMonitor, data, gameSense, menu, popUp, infos):
    error_count = 0
    try:
        while menu.is_alive():
            if bestMonitor.get_timer() >= infos["display_info_time"]:
                bestMonitor.set_timer(0)
                error_count = 0
                time.sleep(infos["display_volume_time"])
            try:
                gameSense.send_event(bestMonitor.get_info_to_send(
                data.get_all_info(), infos["current_event"]))
            except Exception as e:
                error_count = error_count + 1
                if error_count >= infos["display_info_time"] / 2:
                    popUp.error_restart(f"Error while sending data to Sonar.\n" +
                    "Verify that Sonar is still running.\n" +
                    "Otherwise, restart it and click on 'Restart'.\n" +
                    "If it is running, restart it and click on 'Restart'.", f"{e}")
                    sys.exit(1)
                continue
            time.sleep(infos["refresh_rate"])
    except KeyboardInterrupt:
        gameSense.remove_game(bestMonitor.get_game())

def connection(bestMonitor, gameSense, popUp):
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

def test(infos):
    menu = Setting(infos)
    menu.jpp()

def main():
    try:
        popUp = Popup()
        load_env()
        config = load_config_files()
        data = Data()
        gameSense = GameSense()
        bestMonitor = BestMonitor(config)
    except Exception as e:
        popUp.error("Error while initializing the program.\n"+
        "Necessary files are missing or cannot be loaded.\n"+
        "Please check the Program Data.", f"{e}")
        sys.exit(1)
    with multiprocessing.Manager() as manager:
        try:
            infos = manager.dict(config["app_config_values"])
            menu = multiprocessing.Process(target=test, args=(infos,))
            menu.daemon = True
            menu.start()
        except Exception as e:
            popUp.error("son process error", f"{e}")
            sys.exit(1)
        connection(bestMonitor, gameSense, popUp)
        main_loop(bestMonitor, data, gameSense, menu, popUp, infos)
        config.update({"app_config_values": dict(infos)})
        saved_config(popUp, config)


if __name__ == "__main__":
    main()
