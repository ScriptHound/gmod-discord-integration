class MessageFactory:
    def __init__(self, message_dict):
        self.successor = None
        
        if message_dict['t'] == 'MESSAGE_CREATE':
            self.successor = Message(message_dict)

    def get_successor(self):
        return self.successor

class Message:
    def __init__(self, message_dict):
        self.original_data = message_dict

        self.type = message_dict['t']

        self.is_tts = message_dict['d']['tts']
        self.timestamp = message_dict['d']['timestamp']

        self.id = message_dict['d']['id']
        self.flags = message_dict['d']['flags']
        self.embeds = message_dict['d']['embeds']

        self.content = message_dict['d']['content']
        self.from_channel_id = message_dict['d']['channel_id']

        self.author = Author(message_dict['d']['author'])
        self.attachments = message_dict['d']['attachments']

    def get_original_data(self):
        return self.original_data

class Author:
    def __init__(self, data_dict):
        self.username = data_dict['username']
        #self.public_flags = data_dict['public_flags']
        
        self.id = data_dict['id']
        #self.discriminator = data_dict['discriminator']
        
        self.avatar = data_dict['avatar']