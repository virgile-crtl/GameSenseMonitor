from gameSense import GameSense
from data import Data
import time

def main():
    gameSense = GameSense("49845")
    data = Data()
    gameSense.send_event(data.data)
    while True:
        data.get_data()
        print(data.data)
        gameSense.send_event(data.data)

if __name__ == "__main__":
    main()