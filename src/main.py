from gameSense import GameSense
from controller import Controller
from popUp import Popup
from setting import Setting
from data import Data
from utils import *
import multiprocessing, sys

def main_loop(controller, data, gameSense, menu, popUp, infos, config):
    error_count = 1
    try:
        while menu.is_alive():
            try:
                gameSense.send_event(controller.get_info_to_send(
                data.get_all_info(), infos["current_event"]))
            except Exception as e:
                error_count = error_count + 1
                if error_count >= infos["display_info_time"] / 2:
                    popUp.error_restart(f"Error while sending data to Sonar.\n" +
                    "Verify that Sonar is still running.\n" +
                    "Otherwise, restart it and click on 'Restart'.\n" +
                    "If it is running, restart it and click on 'Restart'.", f"{e}", menu)
                    sys.exit(1)
                continue
            time.sleep(infos["refresh_rate"])
            error_count = reset_counter(controller, error_count, infos)
            if config["app_config_values"] != dict(infos):
                config.update({"app_config_values": dict(infos)})
                saved_config(popUp, config)
    except KeyboardInterrupt:
        gameSense.remove_game(controller.get_game())


def main():
    try:
        popUp = Popup()
        config = load_config_files()
        data = Data()
        gameSense = GameSense()
        controller = Controller(config)
    except Exception as e:
        popUp.error("Error while initializing the program.\n"+
        "Necessary files are missing or cannot be loaded.\n"+
        "Please check the Program Data.", f"{e}")
        sys.exit(1)

    with multiprocessing.Manager() as manager:
        try:
            infos = manager.dict(config["app_config_values"])
            menu = multiprocessing.Process(target=Setting, args=(infos, ))
            menu.daemon = True
            menu.start()
        except Exception as e:
            popUp.error("son process error", f"{e}")
            sys.exit(1)
        connection_with_sonar(controller, gameSense, popUp, menu)
        main_loop(controller, data, gameSense, menu, popUp, infos, config)

if __name__ == "__main__":
    main()
