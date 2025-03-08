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
        self.find_adress()
        self.endpoint = Endpoints()

    def find_adress(self):
        try:
            path = os.path.expandvars(os.getenv("ADDRESS_FILE_PATH"))
        except Exception as e:
            my_e = type(e)(f"Error while opening the adress file.\n{e}")
            raise my_e from e
        try:
            file = open(path)
            self.address = 'http://'+json.load(file)['address']
            file.close()
        except Exception as e:
            my_e = type(e)(f"Error while loading the adress.\n{e}")
            raise my_e from e

    def register_game(self, body):
        return self.send_request(self.endpoint.REGISTER_GAME, body)

    def register_event(self, body):
        return self.send_request(self.endpoint.REGISTER_EVENT, body)

    def bind_event(self, body):
        return self.send_request(self.endpoint.BIND_EVENT, body)

    def remove_game(self, body):
        return self.send_request(self.endpoint.REMOVE_GAME, body)

    def remove_event(self, body):
        return self.send_request(self.endpoint.REMOVE_EVENT, body)

    def send_event(self, body):
        return self.send_request(self.endpoint.SEND_EVENT, body)

    def send_request(self, endpoint, body):
        try:
            response = requests.post(self.address + endpoint, json = body)
            response.raise_for_status()
            print("200 OK")
            return 0
        except requests.exceptions.HTTPError as http_err:
            print(f"Error HTTP: {http_err}")
            my_e = type(http_err)(f"Error while sending the request.\n{http_err}")
            raise my_e from http_err
        except requests.exceptions.Timeout:
            print("Error: Timeout")
            my_e = type(http_err)(f"Error while sending the request.\nTimeout")
            raise my_e from http_err
        except requests.exceptions.RequestException as req_err:
            print(f"Request Error: {req_err}")
            my_e = type(req_err)(f"Error while sending the request.\n{req_err}")
            raise my_e from req_err
        except Exception as e:
            print(f"Unexpected Error: {e}")
            my_e = type(e)(f"Error while sending the request.\n{e}")
            raise my_e from e