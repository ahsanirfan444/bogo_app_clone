from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import requests

class MapSocketConsumer(WebsocketConsumer):
    def connect(self):  
        self.accept()


    def receive(self,text_data):
        try:
            text_data_json = json.loads(text_data)
            if isinstance(text_data_json, dict):
                base_url = text_data_json['base_url']
                long = text_data_json['long']
                lat = text_data_json['lat']

                if 'i_subcategory' in text_data_json:
                    i_subcategory = text_data_json['i_subcategory']
                else:
                    i_subcategory = None
                
                if 'user_id' in text_data_json:
                    user_id = text_data_json['user_id']
                    data = {'long': long, 'lat': lat, 'i_subcategory':i_subcategory, 'user_id': user_id}
                else:
                    data = {'long': long, 'lat': lat, 'i_subcategory':i_subcategory}
                

                # Define the API endpoint URL
                url = f'{base_url}api/socket/get_data/'
                

                # Define the headers (if necessary)
                headers = {'Content-Type': 'application/json'}

                # Send the data to the API
                response = requests.post(url, headers=headers, data=json.dumps(data))


                # Check the response status code
                if response.status_code == 200:
                    self.send(text_data=response.text)
                else:
                    self.send(text_data="Something went wrong")


       
        except json.decoder.JSONDecodeError:
            error_message = "Invalid JSON data received"
            self.send(text_data=json.dumps({
                'error': error_message
            }))

class ChatSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_box_name = self.scope['path_remaining']
        self.group_name = "chat_%s" % self.chat_box_name
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    # This function receive messages from WebSocket.

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if isinstance(text_data_json, dict):
            get_data = dict()
            token = text_data_json['token']
            base_url = text_data_json['base_url']
            get_data['receiver_id'] = text_data_json['receiver_id']
            sender_id = text_data_json['sender_id']
            
            get_data['msg_type'] = text_data_json['msg_type']
            get_data['channel_id'] = text_data_json['channel_id']
            get_data['content'] = text_data_json['content']
            get_data['share_data'] = text_data_json['share_data']
            get_data['attachment'] = text_data_json['attachment']


            # Define the API endpoint URL
            url = f'{base_url}api/socket/create_message/'

            

            # Define the headers (if necessary)
            headers = {'Content-Type': 'application/json', 'Authorization': 'JWT '+str(token)}

            # Send the data to the API
            response = requests.post(url, headers=headers, data=json.dumps(get_data))

         

            if response.status_code == 200:
                x= {"type": "chatbox_message"}
                y = text_data_json
                # z = json.loads(x)
                x.update(y)
                await self.channel_layer.group_send(
                    self.group_name,
                    x,
                )

            else:
                await self.send(text_data="Something went wrong")


    async def chatbox_message(self, event):
        #send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                event
            )
        )

    pass