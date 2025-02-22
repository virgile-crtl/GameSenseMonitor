# import time
# from gameSense import GameSense
# from bestMonitor import BestMonitor

# def main():
#     bestMonitor = BestMonitor()
#     gameSense = GameSense()

#     gameSense.register_game(bestMonitor.get_game_info())
#     for event in bestMonitor.get_event_to_register():
#         gameSense.register_event(event)
#     for event in bestMonitor.get_event_to_bind():
#         gameSense.bind_event(event)
#     try:
#         while True:
#             if bestMonitor.get_timer() == 30:
#                 bestMonitor.reset_timer()
#                 time.sleep(5)
#             gameSense.send_event(bestMonitor.get_all_monitor_info())
#             time.sleep(1)
#     except KeyboardInterrupt:
#         gameSense.remove_game(bestMonitor.get_game())

# if __name__ == "__main__":
#     main()

import time
import threading
from pystray import Icon, MenuItem, Menu
from PIL import Image
from gameSense import GameSense
from bestMonitor import BestMonitor

def main_loop():
    """Boucle principale de ton programme qui tourne en arrière-plan."""
    bestMonitor = BestMonitor()
    gameSense = GameSense()

    gameSense.register_game(bestMonitor.get_game_info())
    for event in bestMonitor.get_event_to_register():
        gameSense.register_event(event)
    for event in bestMonitor.get_event_to_bind():
        gameSense.bind_event(event)
    
    try:
        while True:
            if bestMonitor.get_timer() == 30:
                bestMonitor.reset_timer()
                time.sleep(5)
            gameSense.send_event(bestMonitor.get_all_monitor_info())
            time.sleep(1)
    except KeyboardInterrupt:
        gameSense.remove_game(bestMonitor.get_game())

def stop_program(icon, item):
    """Fonction pour quitter proprement depuis l'icône système."""
    icon.stop()

# Charger l'icône (assure-toi d'avoir un fichier icon.ico)
image = Image.open("icon.ico")

# Définir le menu de l'icône
menu = Menu(MenuItem("Quitter", stop_program))

# Créer l'icône dans la zone de notification
icon = Icon("bestMonitor", image, menu=menu)

# Lancer la boucle principale dans un thread séparé
threading.Thread(target=main_loop, daemon=True).start()

# Démarrer l'icône système
icon.run()