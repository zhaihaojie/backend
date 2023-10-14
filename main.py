from fastapi import FastAPI
from typing import List
import asyncio

app = FastAPI()


# 开发restful接口
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/items")
async def create_item(
    name: str = None,
):
    return {"message": "收到请求"}
