from aiohttp import web

from disc_objs.storage import Storage
from disc_objs.disc_api import API
from disc_objs.disc_bot import Bot
from disc_objs.web_gateway import WebGateway

from message_container import MessageFactory

import requests
import json

import websockets
import asyncio

from queue import Queue
import os
import time
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = 'token)'
ANSWER_FOR_HEARTBEAT = '{"t":null,"s":null,"op":11,"d":null}'
MAXIMUM_QUEUE_SIZE = 50
CHANNEL_ID = 'channel_id'
BOT_ID = 'bot_id'

routes = web.RouteTableDef()
app = web.Application()

@routes.post('/send_message')
async def handle_messages_from_gmod(request):
    b = Bot(TOKEN, TEST_CHANNEL)

    request = await request.post()

    name = request.get('name')
    msg = request.get('msg')

    b.send_message(name + ": " + msg)
    logging.info(name, msg, sep='\n')
    return web.Response(text='OK')

@routes.get('/get_messages')
async def get_messages_history(request):
    global q
    if q.qsize() != 0:
        return web.Response(text=str(q.get().get_original_data()))
    else:
        return web.Response(text="No messages")

def put_to_queue(msg, author_id):
    global q
    try: 
        if msg:
            if str(msg.author.id) != author_id:
                q.put(msg)
        
    except TypeError:
        logging.info("An empty message met, ignoring")

def construct_message(json_data, channel_id):
    json_data = json.loads(json_data)
            
    if str(json_data['d']['channel_id']) == channel_id:
        msg = MessageFactory(json_data).get_successor()
        return msg
    
def handle_message(gateway_data, maximum_queue_size):
    if gateway_data != ANSWER_FOR_HEARTBEAT:
        msg = None

        try:
            msg = construct_message(gateway_data, CHANNEL_ID)
            if q.qsize() > maximum_queue_size:
                q.get()

        except TypeError:
            logging.info("JSON expected met NoneType instead")

        put_to_queue(msg, BOT_ID)
        

async def listen(bot, q):
    while True:
        try:
            
            async with websockets.connect(bot.websocket_server_url) as websocket:
                
                websock = WebGateway(bot, websocket)
                await websock.connect_websocket()

                bot.websocket = websocket

                while True:
                    beat_task = asyncio.create_task(websock.heartbeat())
                    message_handle_task = asyncio.create_task(websock.wait_for_message())

                    try:
                        result = await asyncio.gather(beat_task, message_handle_task)
                    except websockets.exceptions.ConnectionClosedOK:
                        logging.info("Discord requested reconnecting...")
                        break
                    
                    handle_message(result[1], MAXIMUM_QUEUE_SIZE)
                    

        except websockets.exceptions.ConnectionClosedError:
            logging.info("Socket was closed, reconnecting...")
            continue

async def run_http_server(host, port):
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()


if __name__ == "__main__":
    
    q = Queue()

    TEST_CHANNEL = CHANNEL_ID

    b = Bot(TOKEN, TEST_CHANNEL)
    b.get_websocket_server()
    
    loop = asyncio.get_event_loop()
    loop.create_task(run_http_server('127.0.0.1', 8881))
    loop.create_task(listen(b, q))
    loop.run_forever()
