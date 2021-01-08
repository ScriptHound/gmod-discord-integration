class Storage():
    def __init__(self, memsize):
        self.memsize = memsize
        self.__storage = []
    
    def save_message(self, message):
        if len(self.__storage) <= self.memsize:
            self.__storage.append(message)
        else:
            self.__storage.pop(0)
            self.__storage.append(message)
    
    def clear_storage(self):
        self.__storage = []

    def pop_message(self):
        return self.__storage.pop(-1)

    def get_storage(self):
        st = self.__storage
        self.__storage = []
        return st