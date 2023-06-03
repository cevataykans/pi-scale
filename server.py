import sys
import time
import threading
import json

from scale import Scale
from typing import Union
from fastapi import FastAPI, Request, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost",
    "http://192.168.0.17"
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
def scale_thread():
    while not exit:
        cur_weight = scale.weight()
        print("Cur weight: ", cur_weight)
        time.sleep(0.1)

threading.Thread(target=scale_thread, name="Scale Thread").start()

@app.on_event("shutdown")
def shutdown_event():
    scale.clean()
    exit = True


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


from fastapi import WebSocket
@app.websocket("/api/v1/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_text(json.dumps({
                "value": cur_weight
            }))
            time.sleep(0.5)
    except WebSocketDisconnect:
        print("Client disconnected")


@app.post("/api/v1/scale", status_code=200)
def tare_again():
    scale.tare()
    print("Scale")
    return {}