import asyncio
import websockets
import json

async def ConnectAndSendToWebsocket(data,url):
    async with websockets.connect(url) as websocket:

        await websocket.send(json.dumps(data))
        print(f"> message Sent")

        message = await websocket.recv()
        print(f"< {message}")


def connect(data,url):
    loop = getOrCreateEventloop()
    loop.run_until_complete(ConnectAndSendToWebsocket(data,url))



def getOrCreateEventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()