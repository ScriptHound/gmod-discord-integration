import json
import requests

TOKEN = 'token)'

def send_requests(channel_id, message):
        endpoint = 'https://discordapp.com/api/'
        token = TOKEN
        channel_id = str(channel_id)
        
        headers = {
            'Authorization' : 'Bot ' + token,
            'Content-Type': 'application/json'    
        }

        content = {
            'content': message
        }

        r = requests.post(endpoint+'channels/'+channel_id+'/messages',
            data=json.dumps(content),
            headers=headers
        )

        print(r)

send_requests(123456789, 'text')