import time
import paho.mqtt.client as mqtt

THINGSBOARD_HOST = '129.126.163.157'
#our token to push into thingsboard
ACCESS_TOKEN = 'vMGW6SoavW0qKjR5AE3D'


client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()
hump = 0
while True:

   hump+=1

   payload="{"
   payload+="\"Total number of Humps detected\":"
   payload += str(hump)
   payload += ","
   payload+="\"SPEED\":"
   #Enter the speed variable or value here convert to string
   payload += str(150)
   payload+="}"
   ret= client.publish("v1/devices/me/telemetry",payload)
   #Check payload inserted into dashboard
   print(payload);
   #Delay and collect data in intervals
   time.sleep(6)

client.loop_stop()
client.disconnect()