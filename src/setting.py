from pystray import MenuItem, Menu, Icon
from PIL import Image
from utils import get_resource_path

class Setting:

    def __init__(self, infos):
        self.infos = infos
        image = Image.open(get_resource_path("assets\\icons\\appIcon.ico"))
        menu = Menu(
            MenuItem('Choose the event to send.',Menu(
                MenuItem('All monitoring info', self.set_current_event("ALL_MONITOR_INFO"), checked=self.get_current_event("ALL_MONITOR_INFO"), radio=True),
                MenuItem('Hour and monitoring info', self.set_current_event("HOUR_TEMP_INFO"), checked=self.get_current_event("HOUR_TEMP_INFO"), radio=True)
            )),
            MenuItem('Refresh rate',Menu(
                MenuItem('1s', self.set_refresh_rate(1), checked=self.get_refresh_rate(1), radio=True),
                MenuItem('2s', self.set_refresh_rate(2), checked=self.get_refresh_rate(2), radio=True),
                MenuItem('3s', self.set_refresh_rate(3), checked=self.get_refresh_rate(3), radio=True),
                MenuItem('5s', self.set_refresh_rate(5), checked=self.get_refresh_rate(5), radio=True),
                MenuItem('10s', self.set_refresh_rate(10), checked=self.get_refresh_rate(10), radio=True)
            )),
            MenuItem('The time to display infos',Menu(
                MenuItem('3s', self.set_display_info_time(3), checked=self.get_display_info_time(3), radio=True),
                MenuItem('15s', self.set_display_info_time(15), checked=self.get_display_info_time(15), radio=True),
                MenuItem('30s', self.set_display_info_time(30), checked=self.get_display_info_time(30), radio=True),
                MenuItem('45s', self.set_display_info_time(45), checked=self.get_display_info_time(45), radio=True),
                MenuItem('60s', self.set_display_info_time(60), checked=self.get_display_info_time(60), radio=True),
            )),
            MenuItem('The time to display volume',Menu(
                MenuItem('1s', self.set_display_vol_time(1), checked=self.get_display_vol_time(1), radio=True),
                MenuItem('3s', self.set_display_vol_time(3), checked=self.get_display_vol_time(3), radio=True),
                MenuItem('5s', self.set_display_vol_time(5), checked=self.get_display_vol_time(5), radio=True),
                MenuItem('10s', self.set_display_vol_time(10), checked=self.get_display_vol_time(10), radio=True),
                MenuItem('15s', self.set_display_vol_time(15), checked=self.get_display_vol_time(15), radio=True),
                MenuItem('never', self.set_display_vol_time(0), checked=self.get_display_vol_time(0), radio=True),

            )),
            MenuItem('Quit', self.quit_action)
        )
        self.icon = Icon("appIcon", image, menu=menu)
        self.icon.run()

    def quit_action(self, icon, item):
        self.icon.stop()

    def set_current_event(self, value):
        def inner(icon, item):
                self.infos["current_event"] = value
                return self.infos["current_event"]
        return inner

    def get_current_event(self, value):
        def inner(item):
                return self.infos["current_event"] == value
        return inner

    def set_display_vol_time(self, value):
        def inner(icon, item):
                self.infos["display_volume_time"] = value
                return self.infos["display_volume_time"]
        return inner

    def get_display_vol_time(self, value):
        def inner(item):
                return self.infos["display_volume_time"] == value
        return inner

    def set_display_info_time(self, value):
        def inner(icon, item):
                self.infos["display_info_time"] = value
                return self.infos["display_info_time"]
        return inner

    def get_display_info_time(self, value):
        def inner(item):
                return self.infos["display_info_time"] == value
        return inner

    def set_refresh_rate(self, value):
        def inner(icon, item):
                self.infos["refresh_rate"] = value
                return self.infos["refresh_rate"]
        return inner

    def get_refresh_rate(self, value):
        def inner(item):
                return self.infos["refresh_rate"] == value
        return inner