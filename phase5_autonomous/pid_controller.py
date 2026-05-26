from phase5_autonomous.constants import PID_INTEGRAL_MAX


class PIDController:
    """
    Generic PID controller. Reused for both lane keeping and speed.

    Usage:
        pid = PIDController(kp=0.04, ki=0.001, kd=0.02)
        output = pid.update(error, dt)

    Call reset() when the control target changes discontinuously
    (e.g. lane change, switching from manual to autonomous).
    """

    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self._integral  = 0.0    # Accumulated error over time
        self._prev_error = None  # Error from previous frame

    def update(self, error, dt=1.0):
        """
        Compute PID output for the given error.

        error : current_target − current_value
        dt    : time delta in seconds (use 1.0 for per-frame calls
                when frame rate is fixed and gains are tuned for it)

        Returns the control output (steering angle, throttle, etc.)
        """
        # ── Proportional term ────────────────────────────────────
        p = self.kp * error

        # ── Integral term (with anti-windup clamp) ───────────────
        self._integral += error * dt
        self._integral  = max(-PID_INTEGRAL_MAX,
                          min( PID_INTEGRAL_MAX, self._integral))
        i = self.ki * self._integral

        # ── Derivative term ──────────────────────────────────────
        if self._prev_error is None:
            # First call: no previous error, derivative is 0
            d = 0.0
        else:
            d = self.kd * (error - self._prev_error) / dt

        self._prev_error = error

        return p + i + d

    def reset(self):
        """Clear accumulated state — call when control target jumps."""
        self._integral   = 0.0
        self._prev_error = None