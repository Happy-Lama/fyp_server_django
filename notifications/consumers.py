from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class NotificationsConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'users'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        
        # sendNotifications.delay()
        print("User connected")
        
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        return super().disconnect(code)
    
    def send_notification(self, event):
        message = event['message']
        self.send(text_data=message)

    def receive(self, text_data=None, bytes_data=None):
        pass