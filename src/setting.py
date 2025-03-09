import os
from dotenv import load_dotenv # type: ignore
import sys
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import multiprocessing
from pystray import Icon, MenuItem, Menu

class Setting:

    def __init__(self, infos):
        self.infos = infos

    def jpp(self):
        image = Image.open(os.getenv("ICON_PATH", ""))
        menu = Menu(
            item('Choose the event to send.',Menu(
                item('All monitoring info', self.set_state("ALL_MONITOR_INFO"), checked=self.get_state("ALL_MONITOR_INFO"), radio=True),
                item('Hour and monitoring info', self.set_state("HOUR_TEMP_INFO"), checked=self.get_state("HOUR_TEMP_INFO"), radio=True)
            )),
            item('Quitter', self.quit_action)
        )
        self.icon = pystray.Icon("BestMonitor", image, menu=menu)
        self.icon.run()

    def quit_action(self, icon, item):
        self.icon.stop()

    def set_state(self, value):
        def inner(icon, item):
                self.infos["current_event"] = value
                return self.infos["current_event"]
        return inner

    def get_state(self, value):
        def inner(item):
                return self.infos["current_event"] == value
        return inner