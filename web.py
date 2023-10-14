from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import asyncio

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_json(data)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "stop":
                await manager.disconnect(websocket)
                await websocket.close()  # 主动关闭连接
                return  # 结束此协程
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


# 模拟 Binance 数据流
async def mock_binance_data_stream():
    while True:
        await asyncio.sleep(0.1)  # 每秒更新一次数据
        price = 10000  # 这只是一个模拟价格，你可以随机生成或使用其他逻辑
        await manager.broadcast({"price": price})


# 在启动时运行模拟数据流
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(mock_binance_data_stream())
