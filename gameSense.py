import requests, os, json , sys

class Endpoints:
    REGISTER_GAME = "/game_metadata"
    REMOVE_GAME = "/remove_game"
    REGISTER_EVENT = "/register_game_event"
    BIND_EVENT = '/bind_game_event'
    REMOVE_EVENT = '/remove_game_event'
    SEND_EVENT = '/game_event'
    HEARTBEAT = '/game_heartbeat'

class GameSense():

    def __init__(self):
        self.address = self.find_adress()
        self.endpoint = Endpoints()

    def find_adress(self):
        try:
            path = os.path.expandvars(r'%programdata%\SteelSeries\SteelSeries Engine 3\coreProps.json')
        except Exception as e:
            print(f"Error while opening the adress file.\n{e}", end="")
            sys.exit()
        try:
            return 'http://'+json.load(open(path))['address']
        except Exception as e:
            print(f"Error while loading the adress.\n{e}", end="")
            sys.exit()

    def register_game(self, body):
        self.send_request(self.endpoint.REGISTER_GAME, body)

    def register_event(self, body):
        self.send_request(self.endpoint.REGISTER_EVENT, body)

    def bind_event(self, body):
        self.send_request(self.endpoint.BIND_EVENT, body)

    def remove_game(self, body):
        self.send_request(self.endpoint.REMOVE_GAME, body)

    def send_event(self, body):
        self.send_request(self.endpoint.SEND_EVENT, body)

    def send_request(self, endpoint, body):
        try:
            response = requests.post(self.address + endpoint, json = body)
            response.raise_for_status()
            print("200 OK")
        except requests.exceptions.HTTPError as http_err:
            print(f"Error HTTP: {http_err}")
        except requests.exceptions.Timeout:
            print("Error: Timeout")
        except requests.exceptions.RequestException as req_err:
            print(f"Request Error: {req_err}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
