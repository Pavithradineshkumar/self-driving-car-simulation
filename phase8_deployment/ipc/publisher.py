# phase8_deployment/ipc/publisher.py

import redis
import json
import time
import os

# Redis connection — reads from environment variable with fallback
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CHANNEL   = "telemetry"


class TelemetryPublisher:
    """
    Publishes car telemetry from Phase 5 to a Redis pub/sub channel.

    Phase 5 (producer process) calls publish() each frame.
    FastAPI (consumer process) subscribes and pushes to WebSocket.

    Redis pub/sub is fire-and-forget:
      - If no subscriber is listening, the message is dropped (not queued)
      - This is fine for live telemetry where stale data has no value
      - Use Redis Streams instead if you need guaranteed delivery/history
    """

    def __init__(self):
        self._client = redis.from_url(REDIS_URL, decode_responses=True)
        self._connected = False
        self._connect()

    def _connect(self):
        try:
            self._client.ping()
            self._connected = True
            print("[TelemetryPublisher] Connected to Redis.")
        except redis.ConnectionError as e:
            print(f"[TelemetryPublisher] WARNING: Redis not available: {e}")
            print("  Dashboard will not receive live telemetry.")
            print("  Start Redis: docker run -d -p 6379:6379 redis:alpine")
            self._connected = False

    def publish(self, telemetry: dict):
        """
        Serialize telemetry dict to JSON and publish to Redis channel.
        Silently skips if Redis is not connected.
        """
        if not self._connected:
            return

        try:
            payload = json.dumps({**telemetry, "ts": time.time()})
            self._client.publish(CHANNEL, payload)
        except redis.ConnectionError:
            # Redis went down mid-session — reconnect next call
            self._connected = False
        except Exception as e:
            print(f"[TelemetryPublisher] Publish error: {e}")

    def close(self):
        self._client.close()


# Module-level singleton — import and use directly
publisher = TelemetryPublisher()