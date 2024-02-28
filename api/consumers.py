from channels.generic.websocket import WebsocketConsumer


class TransformerDataConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
    
    def disconnect(self, code):
        return super().disconnect(code)
    
    def receive(self, text_data=None, bytes_data=None):
        pass


class TransformerSpecificationsConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
    
    def disconnect(self, code):
        return super().disconnect(code)
    
    def receive(self, text_data=None, bytes_data=None):
        pass