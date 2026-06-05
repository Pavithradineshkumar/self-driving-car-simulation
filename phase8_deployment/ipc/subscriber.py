# phase8_deployment/ipc/subscriber.py

import redis
import json
import threading
import os

from phase7_dashboard.backend.data_bridge import bridge

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CHANNEL   = "telemetry"


class TelemetrySubscriber:
    """
    Subscribes to the Redis telemetry channel in a background thread.
    Each message received is written to the DataBridge singleton,
    which FastAPI's WebSocket loop then reads and broadcasts.

    Flow:
        Phase 5 → Redis pub/sub → TelemetrySubscriber → DataBridge
                                                              ↓
                                              FastAPI WebSocket → Browser
    """

    def __init__(self):
        self._running  = False
        self._thread   = None
        self._client   = None

    def start(self):
        """Start background listener thread. Call from FastAPI startup."""
        self._running = True
        self._thread  = threading.Thread(
            target=self._listen_loop,
            daemon=True,
            name="redis-subscriber"
        )
        self._thread.start()
        print("[TelemetrySubscriber] Background listener started.")

    def stop(self):
        self._running = False

    def _listen_loop(self):
        """
        Blocking loop — runs in background thread.
        Reconnects automatically if Redis drops.
        """
        while self._running:
            try:
                client  = redis.from_url(REDIS_URL, decode_responses=True, socket_timeout=None)
                pubsub  = client.pubsub()
                pubsub.subscribe(CHANNEL)
                print(f"[TelemetrySubscriber] Subscribed to '{CHANNEL}'")

                for message in pubsub.listen():

                    if not self._running:
                        break

                    if message["type"] != "message":
                        continue

                    try:
                        data = json.loads(message["data"])
                        bridge.update(data)
                        
                    except (json.JSONDecodeError, KeyError):
                        pass

            except redis.ConnectionError:
                if self._running:
                    print("[TelemetrySubscriber] Redis lost — retrying in 3s")
                    import time
                    time.sleep(3)
            except Exception as e:
                import time
                print(f"[TelemetrySubscriber] Error: {e}")
                time.sleep(1)


subscriber = TelemetrySubscriber()