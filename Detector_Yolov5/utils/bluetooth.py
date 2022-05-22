import obd
import time
from obd import OBDCommand
from obd import OBDResponse
from obd import OBDStatus
from utils.lights import Lights
import paho.mqtt.client as mqtt

# Instruction
# 1. Using Bluetoothctl, we must first pair and trust the OBD2 adapter
# 2. Using RFCOMM (Bluetooth serial connection) to bind the OBD2 adapter to Port 0
# 3. Run the script

#Descriptions
# OBD Protocol is ISO 15765-4 CAN (11 bit ID, 500 kbaud), we need to ensure that the connection parameters are negotiated 
# and established correctly.

class bt:

    #Scanning for the RFCOMM serial connection port that we have set up using Bluetooth control (Bluetoothctl)
    ports = obd.scan_serial()
    print("Ports: ")
    print(ports)

    #Commented out the Logger, used to detect any OBD2 related issues (Connection, query, reponses)
    #obd.logger.setLevel(obd.logging.DEBUG)

    #Initializing the variables and lists needed for the Script

    #Data list used to store the Speed and throttle response from the ECU.
    data_list = []
    #The OBD connection object
    connection = None
    #Initialize the Sense HAT LED Matrix
    ledArray = Lights()

    #Configuration of our ThingsBoard
    THINGSBOARD_HOST = '129.126.163.157'
    ACCESS_TOKEN = 'vMGW6SoavW0qKjR5AE3D'

    def __init__(self):

        #Run method to establish connection between OBD2 sensor and the Engine control unit (ECU)
        self.initialize_OBD()

        #MQTT client (Thingsboard)
        self.client = mqtt.Client()
        self.client.connect(self.THINGSBOARD_HOST, 1883, 60)
        self.client.loop_start()

    def initialize_OBD(self):
        # Init parameters
        #obd_protocol = 6, Commented out protocol as the ECU will auto negotiate
        ports = obd.scan_serial()
        self.connection = obd.OBD(ports[0], baudrate=38400, fast=False, timeout=30)

        # Check status , to remove during actual production
        print(self.connection.status())

    def obd_data(self):

        #Translate to 0b010D (Speed) and 0b0111 (Relative Throttle)
        speedCmd = obd.commands.SPEED
        relative_throttle = obd.commands.RELATIVE_THROTTLE_POS

        self.data_list = []
        if (self.connection.status() != OBDStatus.CAR_CONNECTED):
            self.initialize_OBD()

        #Here we are using a Try-Except loop to catch potential errors
        try:

            # Polling with PID 010D, Speed command from the ECU
            speed_response = self.connection.query(speedCmd)
            # Delay to prevent polling the ECU too quickly which will result in inaccurate responses.
            time.sleep(0.3)
            # Polling with PID 0111, Throttle command from the ECU
            rel_throttle = self.connection.query(relative_throttle)

            
            #Checking if both Speed and Throttle is not None, packets that are empty, should be ignored.
            if (rel_throttle is not None and speed_response is not None):
                self.data_list.append(rel_throttle)
                self.data_list.append(speed_response)
                # payload = "{" + "\"SPEED\":" + str (speed_response.value.magnitude) + "\"Throttle\":" + str (rel_throttle.value.magnitude) +"}" #this is key
                # ret = self.client.publish("v1/devices/me/telemetry", payload)

        except Exception as ex:
            print("Error")
            # Close connection
        # self.connection.close()
        
    def get_reading(self):
        # This method will take in the current reading of speed and throttle position
        # Link to output peripheral (SenseHat) and Buzzer
        speed_threshold_green = 20
        speed_threshold_amber = 30

        throttle_theshold_green = 20
        throttle_theshold_amber = 40

        # Checking if the data list contains the Speed and Throttle object
        if (len(self.data_list) < 2):
            print("Invalid speed and throttle reading")
            return
        # Checking if Speed and Throttle object actually contains value and is not Null
        if (self.data_list[0].value is not None and self.data_list[1].value is not None):

            #Getting the raw speed and raw throttle data
            speed = self.data_list[0].value.magnitude
            throttle_pos = self.data_list[1].value.magnitude

            #Checking if the Spped and throttle is of the correct data type
            #Pass the data into the Decision-making algorithm.
            if (isinstance(speed, float) and isinstance(throttle_pos, float)):
                # print("Speed" + str(speed))
                print("Speed")
                print(speed)
                try:
                    if (speed < speed_threshold_green):
                        if (throttle_pos <= throttle_theshold_green):
                            #Debugging with print statements to ensure the logic flow is correct 
                            print('Output green light')
                            self.ledArray.set_safe()
                            pass
                        else:
                            # Speed within the safe threshold but driver is still engaging Engine Throttle (Exceeds threshold > 20%)
                            if (throttle_pos < throttle_theshold_amber):
                                print('Output amber')
                                self.ledArray.set_warning()
                            # Speed within limit but, Throttle position is way too high (Exceeds threshold > 40%)
                            else:
                                print("THrottle is" +str(throttle_pos))
                                self.ledArray.set_dangerous()
                            pass
                    #Speed is more than Green and less than Amber (Within Amber range)
                    elif (speed > speed_threshold_green and speed < speed_threshold_amber):
                        if (throttle_pos < throttle_theshold_amber):
                            # Driver is within Amber range, set to Warning
                            print('Output amber')
                            self.ledArray.set_warning()
                        else:
                            # Throttle pos too high
                            self.ledArray.set_dangerous()
                            print('Output Red')
                        pass
                    else:
                        # Driver's speed is too fast irregardless of relative throttle position 
                        self.ledArray.set_dangerous()
                        print('Output Red light')

                except Exception as ex:
                    # Close connection
                    # self.connection.close()
                    print("Error: " + str(ex))
