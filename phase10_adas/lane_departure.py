class LaneDepartureWarning:

    SAFE_OFFSET = 60

    def check(self, offset):

        if abs(offset) > self.SAFE_OFFSET:
            return True

        return False