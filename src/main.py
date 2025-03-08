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

def main():
    try:
        popUp = Popup()
        bestMonitor = BestMonitor()
        gameSense = GameSense()
        bestMonitor.check_config_file()
    except Exception as e:
        popUp.error("Error while initializing the program.\n"+
        "Necessary files are missing or cannot be loaded.\n"+
        "Please check the Program Data.", f"{e}")
        sys.exit(1)

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

    error_count = 0
    try:
        while True:
            if bestMonitor.get_timer() >= bestMonitor.get_display_info():
                bestMonitor.set_timer(0)
                error_count = 0
                time.sleep(bestMonitor.get_display_vol())
            try:
                gameSense.send_event(bestMonitor.get_info_to_send())
            except Exception as e:
                error_count = error_count + 1
                if error_count >= bestMonitor.get_display_info() / 2:
                    popUp.error_restart(f"Error while sending data to Sonar.\n" +
                    "Verify that Sonar is still running.\n" +
                    "Otherwise, restart it and click on 'Restart'.\n" +
                    "If it is running, restart it and click on 'Restart'.", f"{e}")
                    sys.exit(1)
                continue
            time.sleep(bestMonitor.get_refresh_rate())
    except KeyboardInterrupt:
        gameSense.remove_game(bestMonitor.get_game())
if __name__ == "__main__":
    main()
