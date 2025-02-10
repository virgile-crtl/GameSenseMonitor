import time
from gameSense import GameSense
from data import Data

def main():
    gameSense = GameSense("MONITOR", "Better Monitoring", "S2xLM2Z")
    data = Data()
    gameSense.send_event(data.data)
    
    while True:
        data.get_data()
        print(data.data)
        gameSense.send_event(data.data)
        time.sleep(1)  # Pause de 1 seconde entre chaque itération

if __name__ == "__main__":
    main()
