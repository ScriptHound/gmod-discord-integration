from flask import Flask, request
from storage import Storage

from disc_api import API
from disc_bot import Bot
from web_gateway import WebGateway
from message_container import MessageFactory

import requests
import json

import websockets
import asyncio

from threading import Thread
from queue import Queue
import os

import time

TOKEN = 'token)'
ANSWER_FOR_HEARTBEAT = '{"t":null,"s":null,"op":11,"d":null}'
MAXIMUM_QUEUE_SIZE = 50
CHANNEL_ID = 'a_channel_id'
BOT_ID = 'a_bot_id'

app = Flask(__name__)

@app.route('/', methods=["POST"])
def hello_world():

    b = Bot(TOKEN, TEST_CHANNEL)

    request.parameter_storage_class = dict
    
    name = request.form['name']
    msg = request.form['msg']

    b.send_message(name + ": " + msg)

    return 'OK'

@app.route('/get_history', methods=['GET'])
def get_history():
    global q
    if q.qsize() != 0:
        return q.get().get_original_data()
    else:
        return "No messages"

@app.route("/signup/", methods = ["POST"])
def signup():
    return "Post request accepted"



def put_to_queue(msg, author_id):
    try: 
        if msg:
            if str(msg.author.id) != author_id:
                q.put(msg)
        
    except TypeError:
        print("An empty message met, ignoring")

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
            print("JSON expected met NoneType instead")

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
                        print("Discord requested reconnecting...")
                        break
                    
                    handle_message(result[1], MAXIMUM_QUEUE_SIZE)
                    

        except websockets.exceptions.ConnectionClosedError:
            print("Socket was closed, reconnecting...")
            continue

def run_http_server(q):
    app.run(host='127.0.0.1', port=8881)

def run_discord_bot(bot, q):
    asyncio.run(listen(bot, q))

if __name__ == "__main__":
    
    q = Queue()

    TEST_CHANNEL = 123456789

    b = Bot(TOKEN, TEST_CHANNEL)
    b.get_websocket_server()

    bot_process = Thread(target=run_discord_bot, args=(b,q,))
    http_process = Thread(target=run_http_server, args=(q,))

    bot_process.start()
    http_process.start()

    bot_process.join()
    http_process.join()