import psutil


class SystemMonitor:

    def get_stats(self):

        return {
            "cpu": round(psutil.cpu_percent(), 1),
            "ram": round(psutil.virtual_memory().percent, 1),
            "backend": "ONLINE"
        }