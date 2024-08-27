class Client:
    def __init__(self, code, client_type, timestamp):
        self.type = client_type     #requested service
        self.code = code            #assigned code 
        self.timestamp = timestamp  #arrival time
    
