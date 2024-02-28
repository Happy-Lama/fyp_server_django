from channels.generic.websocket import WebsocketConsumer

class NotificationsConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        return super().disconnect(code)
    
    def receive(self, text_data=None, bytes_data=None):
        pass