import asyncio
import json

import websockets

from tau.core import NetworkScheduler, MutableSignal
from tau.event import Do


async def subscribe_trades(message_callback):
    uri = "wss://phemex.com/ws"
    async with websockets.connect(uri) as websocket:
        subscribe_msg = {
            'id': 1,
            'method': 'trade.subscribe',
            'params': ['BTCUSD']
        }
        await websocket.send(json.dumps(subscribe_msg))
        while True:
            scheduler.schedule_update(message_callback, await websocket.recv())


messages = MutableSignal()
scheduler = NetworkScheduler()
Do(scheduler.get_network(), messages, lambda: print(f"{messages.get_value()}"))

asyncio.get_event_loop().run_until_complete(subscribe_trades(messages))
