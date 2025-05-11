import ctypes
import sys
import subprocess


class Popup(Exception):

    def error(self, short_message, full_message):
        print(full_message)
        result = ctypes.windll.user32.MessageBoxW(0, f"{short_message}\n\nsee more ?", "GameSenseMonitor", 0x00000014)
        if result == 6:
            ctypes.windll.user32.MessageBoxW(0, full_message, "Détails de l'erreur", 0x00000040)

    def error_restart(self, short_message, full_message, menu):
        print(full_message)
        result = ctypes.windll.user32.MessageBoxW(0, f"{short_message}\n\nsee more (click Continue)?", "GameSenseMonitor", 0x00000016)
        if result == 11:
            result = ctypes.windll.user32.MessageBoxW(0, full_message, "Détails de l'erreur", 0x00000045)
            if result == 4:
                menu.terminate()
                menu.join()
                subprocess.run([sys.executable, sys.argv[0]])
        elif result == 10:
            menu.terminate()
            menu.join()
            subprocess.run([sys.executable, sys.argv[0]])