from gameSense import GameSense
from bestMonitor import BestMonitor
from popUp import Popup
from setting import Setting
from data import Data
from utils import *
import multiprocessing, sys, time

def reset_counter(bestMonitor, error_count, infos):
    if bestMonitor.get_timer() >= infos["display_info_time"]:
        bestMonitor.set_timer(0)
        time.sleep(infos["display_volume_time"])
        return 0
    return error_count

def main_loop(bestMonitor, data, gameSense, menu, popUp, infos):
    error_count = 1
    try:
        while menu.is_alive():
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
            error_count = reset_counter(bestMonitor, error_count, infos)
    except KeyboardInterrupt:
        gameSense.remove_game(bestMonitor.get_game())


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
            menu = multiprocessing.Process(target=Setting, args=(infos, ))
            menu.daemon = True
            menu.start()
        except Exception as e:
            popUp.error("son process error", f"{e}")
            sys.exit(1)
        connection_with_sonar(bestMonitor, gameSense, popUp)
        main_loop(bestMonitor, data, gameSense, menu, popUp, infos)
        config.update({"app_config_values": dict(infos)})
        saved_config(popUp, config)


if __name__ == "__main__":
    main()
