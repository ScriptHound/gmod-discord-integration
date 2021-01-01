import requests
from disc_api import API
from storage import Storage
import json

class Bot():
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        self.websocket = ""

        self.storage = Storage(100)
        self.api = API(self.token, self.channel_id)

    def send_message(self, message):

        content = {
            'content': message
        }
        req, headers = self.api.authorize()

        requests.post(req,
            data=json.dumps(content),
            headers=headers
        )
        
    def get_messages(self):
        content = {
            'limit' : 100
        }

        r, headers = self.api.authorize()
        r = requests.get(r,
            params=content,
            headers=headers
        ).json()
        return r

    def get_websocket_server(self):
        r, headers = self.api.websocket_server_url()

        r = requests.get(r,
            headers=headers
        ).json()
        self.websocket_server_url = r['url']
        self.websocket_server_data = r

    def save_message(self, msg):
        self.storage.save_message(msg)

    def get_message_history(self):
        return self.storage.pop_message()
