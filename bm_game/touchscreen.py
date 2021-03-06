import time
from sys import stdout
from bm_game.XPT2046 import XPT2046

# calibration constants
Y_AT_ZERO = 400
Y_AT_FULL = 2640
X_AT_ZERO = 3850 # x is flipped
X_AT_FULL = 805

class TouchInput():
    """Class to handle the touchscreen input"""

    def __init__(self):
        """Plain constructor
        """
        self.xpt2046 = XPT2046()

    def get_touch_input(self, x_max, y_max):
        """measure and return the input

        Args:
            x_max (int): end of field for x direction
            y_max (int): end of field for y direction
        """

        # first check if the preassure is sensible
        print('Called for measurement')
        preassure = round(self.xpt2046.readTouchPressure(),2)
        if preassure < 0.2 or preassure > 800.0:
            # this is no touch
            return None, None

        print('Touch received')
        # now if the measure is sensible then measure
        x_raw = self.xpt2046.readX()
        y_raw = self.xpt2046.readY()
        print(f'The raw data: x: {x_raw}, y:{y_raw}')

        x_scaled = int((x_raw - X_AT_ZERO) / (X_AT_FULL - X_AT_ZERO) * x_max)
        y_scaled = int((y_raw - Y_AT_ZERO) / (Y_AT_FULL - Y_AT_ZERO) * y_max)
        print(f'The scaled data: x: {x_scaled}, y:{y_scaled}')

        return x_scaled, y_scaled

