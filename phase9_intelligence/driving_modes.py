# phase9_intelligence/driving_modes.py

class DrivingModes:

    ECO = {
        "max_speed": 40,
        "acceleration": 0.5
    }

    NORMAL = {
        "max_speed": 60,
        "acceleration": 1.0
    }

    SPORT = {
        "max_speed": 90,
        "acceleration": 1.5
    }

    current_mode = NORMAL

    @classmethod
    def set_mode(cls, mode):
        cls.current_mode = mode

    @classmethod
    def get_mode(cls):
        return cls.current_mode