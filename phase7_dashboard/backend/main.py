# phase7_dashboard/backend/main.py

import asyncio
import json
from operator import sub
import time

from fastapi                            import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors            import CORSMiddleware
from fastapi.responses                  import StreamingResponse, JSONResponse

from phase7_dashboard.backend.constants import CORS_ORIGINS, WS_INTERVAL
from phase7_dashboard.backend.data_bridge import bridge
from phase7_dashboard.backend.video_stream import video_stream
from phase8_deployment.ipc.subscriber import subscriber

app = FastAPI(title="Self-Driving Car Dashboard API")

# Allow React dev server to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins     = CORS_ORIGINS,
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ── Startup / shutdown ────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    #video_stream.start()
    subscriber.start()
    print("Dashboard backend running at http://localhost:8000")

@app.on_event("shutdown")
async def shutdown():
    video_stream.stop()
    subscriber.stop()
    
# ── REST endpoints ────────────────────────────────────────────────

@app.get("/api/state")
def get_state():
    """Snapshot of current car/agent state. Useful for initial page load."""
    return JSONResponse(content=bridge.snapshot())

@app.get("/api/health")
def health():
    return {"status": "ok", "ts": time.time()}

# ── MJPEG video stream ────────────────────────────────────────────

def _mjpeg_generator():
    """
    Yields MJPEG frames in the multipart/x-mixed-replace format.
    The browser treats each frame as a new image, creating live video.
    """
    while True:
        frame_bytes = video_stream.get_frame()
        if frame_bytes:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame_bytes +
                b"\r\n"
            )
        time.sleep(1 / 30)   # Cap at 30fps

@app.get("/video")
def video_feed():
    return StreamingResponse(
        _mjpeg_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# ── WebSocket — live telemetry ────────────────────────────────────

class ConnectionManager:
    """Tracks all active WebSocket connections."""

    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, data: str):
        dead = []
        for ws in self.active:
            try:
                await ws.send_text(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.active.remove(ws)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Push current state to this client
            snapshot = bridge.snapshot()
            await websocket.send_text(json.dumps(snapshot))
            await asyncio.sleep(WS_INTERVAL)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ── Background broadcaster (pushes to ALL clients) ────────────────

@app.on_event("startup")
async def start_broadcaster():
    asyncio.create_task(_broadcast_loop())

async def _broadcast_loop():
    while True:
        if manager.active:
            snapshot = bridge.snapshot()
            await manager.broadcast(json.dumps(snapshot))
        await asyncio.sleep(WS_INTERVAL)