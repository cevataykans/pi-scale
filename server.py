import sys
import time
import threading
import json
import os
import asyncio
import math

from scale import Scale
from typing import Union
from fastapi import FastAPI, Request, WebSocketDisconnect, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

folder = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory= (folder + "/static").strip() ), name="static")
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost",
    "http://192.168.0.17",
    "http://127.0.0.1"
]

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scale = Scale()
cur_weight = 0
exit = False
tare_lock = threading.Lock()

def scale_thread():
    global cur_weight
    global exit
    while not exit:
        tare_lock.acquire()
        cur_weight = round(scale.weight(), 2)
        if cur_weight < 0:
            cur_weight = 0
        tare_lock.release()
        time.sleep(0.1)

thread = threading.Thread(target=scale_thread, name="Scale Thread")
thread.start()

@app.on_event("shutdown")
def shutdown_event():
    global exit
    exit = True
    thread.join()
    scale.clean()

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/v1/tare")
async def tare():
    print("Tare...")
    tare_lock.acquire()
    scale.tare()
    tare_lock.release()
    return Response(content="Tare Success", media_type="application/text")

from fastapi import WebSocket
@app.websocket("/api/v1/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while not exit:
            await websocket.send_text(json.dumps({
                "value": cur_weight
            }))
            await asyncio.sleep(0.2)
    except WebSocketDisconnect:
        print("Client disconnected")