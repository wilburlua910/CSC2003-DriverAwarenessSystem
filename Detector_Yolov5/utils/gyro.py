from sense_hat import SenseHat
from time import sleep
# from datetime import datetime
# import sys

class gyro:
    senseHat = SenseHat()
    senseHat.low_light = False

    threshold = 3.5 # Threshold for difference between two samples in degrees
    axis = "pitch" # Axis to sample, depending on the mounting position of Pi

    def __init__(self):
        self.runGyro()
        # self.clr()

    # For debugging, flash LED matrix on sense hat 
    # def led(self):
    #     self.senseHat.set_pixels([[255, 192, 203] for i in range(64)])

    # def clr(self):
    #     self.senseHat.clear()

    def runGyro(self):    
        # Sample the gyroscope twice with a delay of 0.5 seconds in between
        # Rationale for delay is that without delay hard to differentiate actual delta from noise

        self.oldSample = self.senseHat.get_gyroscope()
        sleep(0.5)
        self.sample = self.senseHat.get_gyroscope()

        # Calculate the difference between the two samples
        # Rationale for calculating two degrees, 
        #   let oldSample["pitch"] be 1 degree
        #   let sample["pitch"] be 1 359 degree
        #   | 1 - 359 | = 358 degree clockwise
        #   when in reality it could have moved 2 degree counter-clockwise (hump goes up then come down)
        # So to calculate 
        #   | oldSample["pitch"] - sample["pitch"] | and 360 - | oldSample["pitch"] - sample["pitch"] |
        #   and take the minimum
        # Assumption here is the pi or the vehicle doesnt actually rotate 358 degrees

        degreeOne = abs(self.oldSample[axis] - self.sample[axis])
        degreeTwo = 360 - abs(self.oldSample[axis] - self.sample[axis])
        degreeMin = min(degreeOne, degreeTwo)

        # For debugging
        print("d1: %f, d2: %f, dmin: %f" % (degreeOne, degreeTwo, degreeMin))

        # Returns true if the hump detected, consumer to interpret
        if degreeMin > self.threshold:
            # For logging to file
            # timestamp = datetime.now().strftime("%H:%M:%S")
            # print("hump @ %s" % timestamp)
            # self.led()
            # sleep(0.5)
            # self.clr()
            return True
        else:
            return False