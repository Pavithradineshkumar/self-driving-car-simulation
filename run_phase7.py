# python run_phase7.py
import uvicorn
from phase7_dashboard.backend.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)