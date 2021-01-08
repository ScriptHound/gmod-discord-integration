class API():
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        self.endpoint = 'https://discordapp.com/api/'

    def authorize(self):
        
        channel_id = str(self.channel_id)

        headers = {
            'Authorization': 'Bot ' + str(self.token),
            'Content-Type': 'application/json'    
        }
        
        return self.endpoint+'channels/'+channel_id+'/messages', headers

    def websocket_server_url(self):
        headers = {
            'Authorization': 'Bot ' + str(self.token),
            'Content-Type': 'application/json' 
        }

        return self.endpoint+'gateway/bot', headers