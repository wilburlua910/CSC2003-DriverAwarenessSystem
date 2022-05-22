import sense_hat
import threading
import enum

class Lights:
    class _Colors(enum.Enum):
        RED         = (255, 0, 0)
        ORANGE      = (255, 125, 0)
        YELLOW      = (255, 255, 0)
        SPRINGGREEN = (125, 255, 0)
        GREEN       = (0, 255, 0)
        TURQUOISE   = (0, 255, 125)
        CYAN        = (0, 255, 255)
        OCEAN       = (0, 125, 255)
        BLUE        = (0, 0, 255)
        VIOLET      = (125, 0, 255)
        MAGENTA     = (255, 0, 255)
        RASPBERRY   = (255, 0, 125)

    def __init__(self):
        self.sense = sense_hat.SenseHat()
        self.sense.clear()
        self._startup_routine()

    # Indicator that the code is starting up
    def _startup_routine(self):
        self.set_red()
        threading.Timer(0.5, self.set_yellow).start()
        threading.Timer(1, self.set_green).start()

    def low_light_mode(self, enable=True):
        self.sense.low_light = enable

    def set_custom_color(self, color):
        self._set_color(color)

    def set_red(self):
        self._set_color(self._Colors.RED.value)

    set_dangerous = set_red

    def set_yellow(self):
        self._set_color(self._Colors.YELLOW.value)

    set_warning = set_yellow
    
    def set_green(self):
        self._set_color(self._Colors.GREEN.value)

    set_safe = set_green

    def _set_color(self, color):
        for x in range(8):
            for y in range(8):
                self.sense.set_pixel(x, y, color)