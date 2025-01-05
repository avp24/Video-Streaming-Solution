import asyncio
import websockets
import cv2
import base64
from camera import Camera
from httpserver import HttpServer
import signal
import json

camera = Camera(0)
httpserver = HttpServer(8088)
clients = set()

async def handle_browser_message(message):
    """Handles messages from the browser."""
    data = json.loads(message)
    if data.get("action") == "start_recording":
        camera.start_recording(data.get("path", "./recordings"))
    elif data.get("action") == "stop_recording":
        camera.stop_recording()

async def handler(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            await handle_browser_message(message)
    finally:
        clients.remove(websocket)

async def send(websocket):
    frame = camera.get_frame()
    if frame is not None:
        ret, encoded = cv2.imencode(".png", frame)
        if ret:
            base64_frame = base64.b64encode(encoded).decode("ascii")
            try:
                await websocket.send(json.dumps({"frame": base64_frame}))
            except websockets.ConnectionClosed:
                pass

async def broadcast():
    while True:
        for websocket in clients:
            await send(websocket)
        await asyncio.sleep(0.04)

async def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    try:
        httpserver.start()
        camera.start()
        async with websockets.serve(handler, "", 8089):
            await broadcast()
    except (KeyboardInterrupt, asyncio.CancelledError):
        httpserver.stop()
        camera.stop()

if __name__ == "__main__":
    asyncio.run(main())

