# phase7_dashboard/backend/constants.py

HOST            = "0.0.0.0"
PORT            = 8000

# How often to push data over WebSocket (seconds)
WS_INTERVAL     = 0.05     # 20 updates/sec

# Video stream
MJPEG_QUALITY   = 80       # JPEG compression quality (1–100)

# CORS origins allowed (React dev server)
CORS_ORIGINS    = [
    "http://localhost:5173",   # Vite default
    "http://localhost:3000",
]