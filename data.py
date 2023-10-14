import asyncio
import websockets
import json


async def receive_binance_data():
    uri = "wss://stream.binancefuture.com/ws/btcusdt_perpetual@continuousKline_1m"
    async with websockets.connect(uri) as websocket:
        while True:
            await asyncio.sleep(0.1)  # 每秒更新一次数据
            response = await websocket.recv()
            data = json.loads(response)
            print(data)  # 输出从 Binance 接收到的数据


asyncio.get_event_loop().run_until_complete(receive_binance_data())
