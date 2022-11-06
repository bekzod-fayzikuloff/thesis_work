import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class CallConsumer(WebsocketConsumer):
    my_name = "Foo"

    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({"type": "connection", "data": {"message": "Connected"}}))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.my_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        print(f"Receiving text data: {text_data}")
        text_data_json = json.loads(text_data)

        event_type = text_data_json["type"]

        if event_type == "login":
            print(f"login event type")
            name = text_data_json["data"]["name"]

            self.my_name = name
            async_to_sync(self.channel_layer.group_add)(self.my_name, self.channel_name)
        if event_type == "call":
            print(f"Call event type")
            name = text_data_json["data"]["name"]
            print(self.my_name, "is calling", name)

            async_to_sync(self.channel_layer.group_send)(
                name,
                {
                    "type": "call_received",
                    "data": {"caller": self.my_name, "rtcMessage": text_data_json["data"]["rtcMessage"]},
                },
            )

        if event_type == "answer_call":
            print(f"Answer call event type")
            caller = text_data_json["data"]["caller"]
            print(self.my_name, "is answering", caller, "calls.")

            async_to_sync(self.channel_layer.group_send)(
                caller, {"type": "call_answered", "data": {"rtcMessage": text_data_json["data"]["rtcMessage"]}}
            )

        if event_type == "ICEcandidate":
            user = text_data_json["data"]["user"]

            async_to_sync(self.channel_layer.group_send)(
                user, {"type": "ICEcandidate", "data": {"rtcMessage": text_data_json["data"]["rtcMessage"]}}
            )

            print(f"ICE candidate event type")

    def call_received(self, event):
        self.send(text_data=json.dumps({"type": "call_received", "data": event["data"]}))

    def call_answered(self, event):
        self.send(text_data=json.dumps({"type": "call_answered", "data": event["data"]}))

    def ICEcandidate(self, event):
        self.send(text_data=json.dumps({"type": "ICEcandidate", "data": event["data"]}))
