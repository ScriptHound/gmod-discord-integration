import json
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

class WebGateway:
    def __init__(self, bot, websocket):
        self.token = bot.token
        self.bot = bot
        self.websocket = websocket

    async def __acknowledge_heartbeat(self):
        await self.websocket.send(json.dumps({
                "op": 1,
                "d": "null"
            }
        ))

        r = json.loads(await self.websocket.recv())

        if r["op"] == 11:
            logging.info("heartbeat was acknowledged")
        else:
            logging.info(r, "Heartbeat was not acknowledged")

    async def connect_websocket(self):
        r = await self.websocket.recv()
        logging.info(r)

        await self.__acknowledge_heartbeat()

        propeties = {
            "$os": "linux",
            "$browser": "gaige_brower",
            "$device": "deathtrap"
        }

        #intents 513 is a subscibtion to events:
        #messages
        await self.websocket.send(json.dumps({
                "op": 2,
                "d": {
                    "token": self.bot.token,
                    "intents": 513,
                    "properties": propeties
                }
            })
        )
        json.dumps(json.loads(await self.websocket.recv()), indent=4)
        logging.info("Connection created")

    async def heartbeat(self):
    
        await self.websocket.send(json.dumps({
                "op": 1,
                "d": "null"
            }
        ))

        json.dumps(json.loads(await self.websocket.recv()), indent=4)
        
        logging.info("Heartbeat has been sent")

    async def wait_for_message(self):
        await asyncio.sleep(1)
        logging.info("Waiting for a message")
        
        try:
            data = await asyncio.wait_for(self.websocket.recv(), timeout=35)
            r = json.dumps(json.loads(data), indent=4)

            self.bot.save_message(r)

            return data
        
        except asyncio.TimeoutError:
            logging.info("Timeout reached")